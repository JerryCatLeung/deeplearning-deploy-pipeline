package com.jason.mlsvconnx.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;


import ai.onnxruntime.OnnxTensor;
import ai.onnxruntime.OnnxValue;
import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtException;
import ai.onnxruntime.OrtSession;
import ai.onnxruntime.OrtSession.Result;
import ai.onnxruntime.OrtSession.SessionOptions;

import java.nio.FloatBuffer;
import java.nio.LongBuffer;

@Component
public class TestOnnxModel implements InitializingBean {

    private OrtSession session;
    private OrtEnvironment env;

    @Value("${onnxruntime.inter-op-num-threads:1}")
    private int interOpNumThreads;

    private static final String ENV_TEST_MODEL_PATH = "TEST_MODEL_PATH";

    @Override
    public void afterPropertiesSet() throws Exception {
        String modelPath = System.getenv(ENV_TEST_MODEL_PATH);
        if (modelPath == null) {
            throw new Exception("Environment variable " + ENV_TEST_MODEL_PATH + " is not set");
        }
        OrtSession.SessionOptions opts = new SessionOptions();
        opts.setInterOpNumThreads(interOpNumThreads);
        this.env = OrtEnvironment.getEnvironment();
        this.session = env.createSession(modelPath, opts);
    }

    public List<float[]> predict(long[] featIds, float[] featVals, long[] shape) throws Exception {
        Map<String, OnnxTensor> inputs = new HashMap<>();

        inputs.put("feat_ids", OnnxTensor.createTensor(env, LongBuffer.wrap(featIds), shape));
        inputs.put("feat_vals", OnnxTensor.createTensor(env, FloatBuffer.wrap(featVals), shape));

        List<float[]> rsList = new ArrayList<>();
        Result result = session.run(inputs);
        result.forEach(entry -> {
            OnnxValue value = (OnnxValue) entry.getValue();
            try {
                float[] rs = (float[]) value.getValue();
                rsList.add(rs);
            } catch (OrtException e) {
                rsList.add(new float[] {});
            }
        });

        return rsList;
    }

}
