package com.jason.mlsvconnx.grpc;

import com.jason.mlsvconnx.proto.ModelGrpc.ModelImplBase;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import com.jason.mlsvconnx.model.TestOnnxModel;
import com.jason.mlsvconnx.proto.ModelReply;
import com.jason.mlsvconnx.proto.ModelRequest;
import io.grpc.stub.StreamObserver;
import net.devh.boot.grpc.server.service.GrpcService;

@GrpcService
public class ModelGrpcService extends ModelImplBase {

    @Autowired
    private TestOnnxModel testOnnxModel;

    @Override
    public void runModel(ModelRequest request, StreamObserver<ModelReply> responseObserver) {
        long[] feat_ids = request.getInput1List().stream().mapToLong(i -> i).toArray();
        float[] feat_vals = list2Array(request.getInput2List());
        long[] shapt = new long[] {feat_ids.length / 39l, 39l };
        try {
            com.jason.mlsvconnx.proto.ModelReply.Builder replyBuilder = ModelReply.newBuilder();
            List<float[]> result = testOnnxModel.predict(feat_ids, feat_vals, shapt);
            result.forEach(entry -> {
                for (int i = 0; i < entry.length; i++) {
                    replyBuilder.addOutput(entry[i]);
                }
            });
            responseObserver.onNext(replyBuilder.build());
        } catch (Exception e) {
            System.out.println(e);
        }

        responseObserver.onCompleted();
    }

    public float[] list2Array(List<Float> list) {
        float[] array = new float[list.size()];
        for (int i = 0; i < list.size(); i++) {
            array[i] = list.get(i);
        }
        return array;
    }
}
