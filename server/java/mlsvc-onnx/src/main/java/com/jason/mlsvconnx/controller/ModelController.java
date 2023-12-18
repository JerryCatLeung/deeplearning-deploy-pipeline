package com.jason.mlsvconnx.controller;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.jason.mlsvconnx.model.TestOnnxModel;

import lombok.Data;

@RestController
@RequestMapping("/model")
public class ModelController {

    @Autowired
    private TestOnnxModel testOnnxModel;
    
    private static final List<float[]> EMPTY_LIST = new ArrayList<>();

    @PostMapping("/onnx/infer")
    public List<float[]> treeliteInfer(@RequestBody ModelRequest params) throws Exception {
        if (params.getFeat_ids() != null && params.getFeat_vals() != null) {
            return testOnnxModel.predict(params.getFeat_ids(), params.getFeat_vals(), params.getShape());
        }
        return EMPTY_LIST;
    }

    @Data
    public static class ModelRequest {
        long[] feat_ids;
        float[] feat_vals;
        long[] shape;
    }

}