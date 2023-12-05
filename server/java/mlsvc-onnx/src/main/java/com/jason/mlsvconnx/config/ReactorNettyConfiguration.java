package com.jason.mlsvconnx.config;

import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.http.client.reactive.ReactorResourceFactory;
import org.springframework.stereotype.Component;

import lombok.Data;
import reactor.netty.ReactorNetty;

@Configurable
public class ReactorNettyConfiguration {

    @Bean
    @ConditionalOnBean(ReactorNettyProperties.class)
    public ReactorResourceFactory reactorResourceFactory(ReactorNettyProperties reactorNettyProperties) {
        if (reactorNettyProperties.getIoSelectCount() > 0) {
            System.setProperty(ReactorNetty.IO_SELECT_COUNT, String.valueOf(reactorNettyProperties.getIoSelectCount()));
        }
        if (reactorNettyProperties.getIoWorkerCount() > 0) {
            System.setProperty(ReactorNetty.IO_WORKER_COUNT, String.valueOf(reactorNettyProperties.getIoWorkerCount()));
        }
        return new ReactorResourceFactory();
    }

    @Data
    @Component
    @ConfigurationProperties(prefix = "reactor.netty")
    public static class ReactorNettyProperties {
        private int ioWorkerCount = Runtime.getRuntime().availableProcessors() + 1;
        private int ioSelectCount = 1;
    }
    
}
