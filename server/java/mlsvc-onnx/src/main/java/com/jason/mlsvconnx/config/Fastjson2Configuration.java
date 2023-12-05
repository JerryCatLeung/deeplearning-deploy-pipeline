package com.jason.mlsvconnx.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.core.codec.Decoder;
import org.springframework.core.codec.Encoder;
import org.springframework.http.codec.ServerCodecConfigurer;
import org.springframework.util.MimeTypeUtils;
import org.springframework.web.reactive.config.WebFluxConfigurer;

import com.alibaba.fastjson2.PropertyNamingStrategy;
import com.alibaba.fastjson2.filter.NameFilter;
import com.alibaba.fastjson2.support.config.FastJsonConfig;
import com.alibaba.fastjson2.support.spring.http.codec.Fastjson2Decoder;
import com.alibaba.fastjson2.support.spring.http.codec.Fastjson2Encoder;
import com.alibaba.fastjson2.support.spring.http.converter.FastJsonHttpMessageConverter;
import com.fasterxml.jackson.databind.ObjectMapper;

import lombok.Data;

@Data
@ConditionalOnClass(FastJsonHttpMessageConverter.class)
public class Fastjson2Configuration implements WebFluxConfigurer {

    @Autowired
    private ObjectMapper objectMapper;

    @Override
    public void configureHttpMessageCodecs(ServerCodecConfigurer configurer) {
        WebFluxConfigurer.super.configureHttpMessageCodecs(configurer);
        FastJsonConfig fastJsonConfig = new FastJsonConfig();
        
        fastJsonConfig.setReaderFilters(NameFilter.of(PropertyNamingStrategy.SnakeCase));
        fastJsonConfig.setWriterFilters(NameFilter.of(PropertyNamingStrategy.SnakeCase));

        Encoder fastEncoder = new Fastjson2Encoder(objectMapper, fastJsonConfig, MimeTypeUtils.APPLICATION_JSON);
        Decoder fastDecoder = new Fastjson2Decoder(objectMapper, fastJsonConfig, MimeTypeUtils.APPLICATION_JSON);
        configurer.defaultCodecs().jackson2JsonEncoder(fastEncoder);
        configurer.defaultCodecs().jackson2JsonDecoder(fastDecoder);
    }

}