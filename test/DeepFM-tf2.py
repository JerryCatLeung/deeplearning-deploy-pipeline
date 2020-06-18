import glob
import json
import os
import random
import shutil
from datetime import date, timedelta

import tensorflow as tf

#################### CMD Arguments ####################
FLAGS = tf.compat.v1.flags.FLAGS
tf.compat.v1.flags.DEFINE_integer("dist_mode", 0, "distribution mode {0-local, 1-single_dist, 2-multi_dist}")
tf.compat.v1.flags.DEFINE_string("ps_hosts", '', "Comma-separated list of hostname:port pairs")
tf.compat.v1.flags.DEFINE_string("worker_hosts", '', "Comma-separated list of hostname:port pairs")
tf.compat.v1.flags.DEFINE_string("job_name", '', "One of 'ps', 'worker'")
tf.compat.v1.flags.DEFINE_integer("task_index", 0, "Index of task within the job")
tf.compat.v1.flags.DEFINE_integer("num_threads", 16, "Number of threads")
tf.compat.v1.flags.DEFINE_integer("feature_size", 0, "Number of features")
tf.compat.v1.flags.DEFINE_integer("field_size", 0, "Number of fields")
tf.compat.v1.flags.DEFINE_integer("embedding_size", 32, "Embedding size")
tf.compat.v1.flags.DEFINE_integer("num_epochs", 10, "Number of epochs")
tf.compat.v1.flags.DEFINE_integer("batch_size", 64, "Number of batch size")
tf.compat.v1.flags.DEFINE_integer("log_steps", 1000, "save summary every steps")
tf.compat.v1.flags.DEFINE_float("learning_rate", 0.0005, "learning rate")
tf.compat.v1.flags.DEFINE_float("l2_reg", 0.0001, "L2 regularization")
tf.compat.v1.flags.DEFINE_string("loss_type", 'log_loss', "loss type {square_loss, log_loss}")
tf.compat.v1.flags.DEFINE_string("optimizer", 'Adam', "optimizer type {Adam, Adagrad, GD, Momentum}")
tf.compat.v1.flags.DEFINE_string("deep_layers", '256,128,64', "deep layers")
tf.compat.v1.flags.DEFINE_string("dropout", '0.5,0.5,0.5', "dropout rate")
tf.compat.v1.flags.DEFINE_boolean("batch_norm", False, "perform batch normalization (True or False)")
tf.compat.v1.flags.DEFINE_float("batch_norm_decay", 0.9, "decay for the moving average(recommend trying decay=0.9)")
tf.compat.v1.flags.DEFINE_string("data_dir", '', "data dir")
tf.compat.v1.flags.DEFINE_string("dt_dir", '', "data dt partition")
tf.compat.v1.flags.DEFINE_string("model_dir", '', "model check point dir")
tf.compat.v1.flags.DEFINE_string("servile_model_dir", '', "export servile model for TensorFlow Serving")
tf.compat.v1.flags.DEFINE_string("task_type", 'train', "task type {train, infer, eval, export}")
tf.compat.v1.flags.DEFINE_boolean("clear_existing_model", False, "clear existing model or not")


# 1 1:0.5 2:0.03519 3:1 4:0.02567 7:0.03708 8:0.01705 9:0.06296 10:0.18185 11:0.02497 12:1 14:0.02565 15:0.03267
#   17:0.0247 18:0.03158 20:1 22:1 23:0.13169 24:0.02933 27:0.18159 31:0.0177 34:0.02888 38:1 51:1 63:1 132:1 164:1
#   236:1
def input_fn(filename, batch_size=64):
    print("Parsing", filename)

    def parse_libsvm(line):
        columns = tf.strings.split([line], ' ')
        labels = tf.strings.to_number(columns.values[0], out_type=tf.float32)
        splits = tf.strings.split(columns.values[1:], ':')
        id_vals = splits.to_tensor()
        feat_ids, feat_vals = tf.split(id_vals, num_or_size_splits=2, axis=1)
        feat_ids = tf.strings.to_number(feat_ids, out_type=tf.int32)
        feat_vals = tf.strings.to_number(feat_vals, out_type=tf.float32)
        return {"feat_ids": feat_ids, "feat_vals": feat_vals}, labels

    # Extract lines from input files using the Dataset API, can pass one filename or filename list
    dataset = tf.data.TextLineDataset(filename)
    dataset = dataset.map(map_func=parse_libsvm, num_parallel_calls=10).prefetch(buffer_size=50000)  # multi-thread
    # pre-process then prefetch
    dataset = dataset.shuffle(buffer_size=1000)
    # epochs from blending together. default is ever
    dataset = dataset.repeat()
    dataset = dataset.batch(batch_size)

    # return dataset.make_one_shot_iterator()
    iterator = tf.compat.v1.data.make_one_shot_iterator(dataset)
    batch_features, batch_labels = iterator.get_next()
    # return tf.reshape(batch_ids,shape=[-1,field_size]), tf.reshape(batch_vals,shape=[-1,field_size]), batch_labels
    return batch_features, batch_labels


def model_fn(features, labels, mode, params):
    """Build Model Function f(x) for Estimator"""
    # ------hyper parameters------
    field_size = params["field_size"]
    feature_size = params["feature_size"]
    embedding_size = params["embedding_size"]
    l2_reg = params["l2_reg"]
    learning_rate = params["learning_rate"]
    layers = list(map(int, params["deep_layers"].split(",")))
    dropout = list(map(int, params["dropout"].split(",")))

    # ------build weights------
    FM_B = tf.compat.v1.get_variable(name="fm_bias", shape=[1], initializer=tf.constant_initializer(0.0))
    FM_W = tf.compat.v1.get_variable(name="fm_w", shape=[feature_size],
                                     initializer=tf.compat.v1.glorot_normal_initializer())
    FM_V = tf.compat.v1.get_variable(name="fm_v", shape=[feature_size, embedding_size],
                                     initializer=tf.compat.v1.glorot_normal_initializer())

    # ------build features------
    feat_ids = features["feat_ids"]
    feat_ids = tf.reshape(feat_ids, shape=[-1, field_size])
    feat_vals = features["feat_vals"]
    feat_vals = tf.reshape(feat_vals, shape=[-1, field_size])

    # ------build f(x)------
    with tf.compat.v1.variable_scope("first_order"):
        feat_weights = tf.nn.embedding_lookup(FM_W, ids=feat_ids)  # None * field_size * 1
        y_w = tf.reduce_sum(tf.multiply(feat_weights, feat_vals), axis=1)

    with tf.compat.v1.variable_scope("second_order"):
        embeddings = tf.nn.embedding_lookup(FM_V, ids=feat_ids)  # None * field_size * k
        feat_vals = tf.reshape(feat_vals, shape=[-1, field_size, 1])
        embeddings = tf.multiply(embeddings, feat_vals)  # vij*xi
        sum_square = tf.square(tf.reduce_sum(embeddings, 1))
        square_sum = tf.reduce_sum(tf.square(embeddings), 1)
        y_v = 0.5 * tf.reduce_sum(tf.subtract(sum_square, square_sum), 1)  # None * 1

    with tf.compat.v1.variable_scope("deep_part"):
        deep_inputs = tf.reshape(embeddings, shape=[-1, field_size * embedding_size])  # None * (field_size*k)
        for i in range(len(layers)):
            deep_inputs = tf.keras.layers.Dense(units=layers[i], activation="relu")(deep_inputs)
        deep_inputs = tf.keras.layers.Dense(units=1, activation="relu",
                                            kernel_regularizer=tf.keras.regularizers.l2(l2_reg),
                                            name="deep_output")(deep_inputs)
        y_d = deep_inputs

    with tf.compat.v1.variable_scope("DeepFM-out"):
        y_bias = FM_B * tf.ones_like(y_d, dtype=tf.float32)  # None * 1
        y = y_bias + y_w + y_v + y_d
        pred = tf.sigmoid(y)

    predictions = {"prob": pred}
    export_outputs = {
        tf.compat.v1.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: tf.estimator.export.PredictOutput(
            predictions)}
    # Provide an estimator spec for `ModeKeys.PREDICT`
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predictions,
            export_outputs=export_outputs
        )

    # ------build loss------
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=y, labels=labels)) + \
           l2_reg * tf.nn.l2_loss(FM_W) + \
           l2_reg * tf.nn.l2_loss(FM_V)

    # Provide an estimator spec for `ModeKeys.EVAL`
    eval_metric_ops = {
        "auc": tf.compat.v1.metrics.auc(labels, pred)
    }
    if mode == tf.estimator.ModeKeys.EVAL:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predictions,
            loss=loss,
            eval_metric_ops=eval_metric_ops
        )
    # ------build optimizer------
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate, beta1=0.9, beta2=0.999, epsilon=1e-8)
    train_op = optimizer.minimize(loss, global_step=tf.compat.v1.train.get_global_step())

    # Provide an estimator spec for `ModeKeys.TRAIN` modes
    if mode == tf.estimator.ModeKeys.TRAIN:
        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=predictions,
            loss=loss,
            train_op=train_op
        )


def set_dist_env():
    if FLAGS.dist_mode == 1:  # 本地分布式测试模式1 chief, 1 ps, 1 evaluator
        ps_hosts = FLAGS.ps_hosts.split(',')
        chief_hosts = FLAGS.chief_hosts.split(',')
        task_index = FLAGS.task_index
        job_name = FLAGS.job_name
        print('ps_host', ps_hosts)
        print('chief_hosts', chief_hosts)
        print('job_name', job_name)
        print('task_index', str(task_index))
        # 无worker参数
        tf_config = {
            'cluster': {'chief': chief_hosts, 'ps': ps_hosts},
            'task': {'type': job_name, 'index': task_index}
        }
        print(json.dumps(tf_config))
        os.environ['TF_CONFIG'] = json.dumps(tf_config)
    elif FLAGS.dist_mode == 2:  # 集群分布式模式
        ps_hosts = FLAGS.ps_hosts.split(',')
        worker_hosts = FLAGS.worker_hosts.split(',')
        chief_hosts = worker_hosts[0:1]  # get first worker as chief
        worker_hosts = worker_hosts[2:]  # the rest as worker
        task_index = FLAGS.task_index
        job_name = FLAGS.job_name
        print('ps_host', ps_hosts)
        print('worker_host', worker_hosts)
        print('chief_hosts', chief_hosts)
        print('job_name', job_name)
        print('task_index', str(task_index))
        # use #worker=0 as chief
        if job_name == "worker" and task_index == 0:
            job_name = "chief"
        # use #worker=1 as evaluator
        if job_name == "worker" and task_index == 1:
            job_name = 'evaluator'
            task_index = 0
        # the others as worker
        if job_name == "worker" and task_index > 1:
            task_index -= 2

        tf_config = {
            'cluster': {'chief': chief_hosts, 'worker': worker_hosts, 'ps': ps_hosts},
            'task': {'type': job_name, 'index': task_index}
        }
        print(json.dumps(tf_config))
        os.environ['TF_CONFIG'] = json.dumps(tf_config)


def main(_):
    # ------check Arguments------
    if FLAGS.dt_dir == "":
        FLAGS.dt_dir = (date.today() + timedelta(-1)).strftime('%Y%m%d')
    FLAGS.model_dir = FLAGS.model_dir + FLAGS.dt_dir
    # FLAGS.data_dir  = FLAGS.data_dir + FLAGS.dt_dir

    print('task_type ', FLAGS.task_type)
    print('model_dir ', FLAGS.model_dir)
    print('data_dir ', FLAGS.data_dir)
    print('dt_dir ', FLAGS.dt_dir)
    print('num_epochs ', FLAGS.num_epochs)
    print('feature_size ', FLAGS.feature_size)
    print('field_size ', FLAGS.field_size)
    print('embedding_size ', FLAGS.embedding_size)
    print('batch_size ', FLAGS.batch_size)
    print('deep_layers ', FLAGS.deep_layers)
    print('dropout ', FLAGS.dropout)
    print('loss_type ', FLAGS.loss_type)
    print('optimizer ', FLAGS.optimizer)
    print('learning_rate ', FLAGS.learning_rate)
    print('batch_norm_decay ', FLAGS.batch_norm_decay)
    print('batch_norm ', FLAGS.batch_norm)
    print('l2_reg ', FLAGS.l2_reg)

    # ------init Envs------
    tr_files = glob.glob("%s/tr*libsvm" % FLAGS.data_dir)
    random.shuffle(tr_files)
    print("tr_files:", tr_files)
    va_files = glob.glob("%s/va*libsvm" % FLAGS.data_dir)
    print("va_files:", va_files)
    te_files = glob.glob("%s/te*libsvm" % FLAGS.data_dir)
    print("te_files:", te_files)

    if FLAGS.clear_existing_model:
        try:
            shutil.rmtree(FLAGS.model_dir)
        except Exception as e:
            print(e, "at clear_existing_model")
        else:
            print("existing model cleaned at %s" % FLAGS.model_dir)

    set_dist_env()
    # ------build Tasks------
    model_params = {
        "field_size": FLAGS.field_size,
        "feature_size": FLAGS.feature_size,
        "embedding_size": FLAGS.embedding_size,
        "learning_rate": FLAGS.learning_rate,
        "batch_norm_decay": FLAGS.batch_norm_decay,
        "l2_reg": FLAGS.l2_reg,
        "deep_layers": FLAGS.deep_layers,
        "dropout": FLAGS.dropout
    }

    config = tf.estimator.RunConfig().replace(
        session_config=tf.compat.v1.ConfigProto(device_count={"GPU": 0, "CPU": FLAGS.num_Threads}),
        log_step_count_steps=FLAGS.log_steps,
        save_summary_steps=FLAGS.log_steps
    )

    DeepFM = tf.estimator.Estimator(model_fn=model_fn, model_dir=FLAGS.model_dir, params=model_params, config=config)

    if FLAGS.task_type == "train":
        train_spec = tf.estimator.TrainSpec(input_fn=lambda: input_fn(filename=tr_files, batch_size=FLAGS.batch_size))
        eval_spec = tf.estimator.EvalSpec(input_fn=lambda: input_fn(filename=va_files, batch_size=FLAGS.batch_size),
                                          steps=None, start_delay_secs=1000, throttle_secs=1200)
        tf.estimator.train_and_evaluate(DeepFM, train_spec, eval_spec)
    elif FLAGS.task_type == "eval":
        DeepFM.evaluate(input_fn=lambda: input_fn(filename=va_files, batch_size=FLAGS.batch_size))
    elif FLAGS.task_type == "infer":
        preds = DeepFM.predict(input_fn=lambda: input_fn(filename=te_files, batch_size=FLAGS.batch_size),
                               predict_keys="prob")
        with open(FLAGS.data_dir + "/pred.txt", "w") as fo:
            for prob in preds:
                fo.write("%f\n" % (prob['prob']))
    elif FLAGS.task_type == "export":
        feature_spec = {
            'feat_ids': tf.compat.v1.placeholder(dtype=tf.int64, shape=[None, FLAGS.field_size], name='feat_ids'),
            'feat_vals': tf.compat.v1.placeholder(dtype=tf.float32, shape=[None, FLAGS.field_size], name='feat_vals')
        }
        serving_input_receiver_fn = tf.estimator.export.build_raw_serving_input_receiver_fn(feature_spec)
        DeepFM.export_savedmodel(FLAGS.servile_model_dir, serving_input_receiver_fn)


if __name__ == "__main__":
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.info)
    tf.compat.v1.app.run()
