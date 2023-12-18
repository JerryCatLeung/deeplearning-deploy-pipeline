package com.jason.mlsvconnx.proto;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.56.0)",
    comments = "Source: model.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class ModelGrpc {

  private ModelGrpc() {}

  public static final String SERVICE_NAME = "model.Model";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<com.jason.mlsvconnx.proto.ModelRequest,
      com.jason.mlsvconnx.proto.ModelReply> getRunModelMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "RunModel",
      requestType = com.jason.mlsvconnx.proto.ModelRequest.class,
      responseType = com.jason.mlsvconnx.proto.ModelReply.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<com.jason.mlsvconnx.proto.ModelRequest,
      com.jason.mlsvconnx.proto.ModelReply> getRunModelMethod() {
    io.grpc.MethodDescriptor<com.jason.mlsvconnx.proto.ModelRequest, com.jason.mlsvconnx.proto.ModelReply> getRunModelMethod;
    if ((getRunModelMethod = ModelGrpc.getRunModelMethod) == null) {
      synchronized (ModelGrpc.class) {
        if ((getRunModelMethod = ModelGrpc.getRunModelMethod) == null) {
          ModelGrpc.getRunModelMethod = getRunModelMethod =
              io.grpc.MethodDescriptor.<com.jason.mlsvconnx.proto.ModelRequest, com.jason.mlsvconnx.proto.ModelReply>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "RunModel"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.jason.mlsvconnx.proto.ModelRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  com.jason.mlsvconnx.proto.ModelReply.getDefaultInstance()))
              .setSchemaDescriptor(new ModelMethodDescriptorSupplier("RunModel"))
              .build();
        }
      }
    }
    return getRunModelMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ModelStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ModelStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ModelStub>() {
        @java.lang.Override
        public ModelStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ModelStub(channel, callOptions);
        }
      };
    return ModelStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ModelBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ModelBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ModelBlockingStub>() {
        @java.lang.Override
        public ModelBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ModelBlockingStub(channel, callOptions);
        }
      };
    return ModelBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ModelFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<ModelFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<ModelFutureStub>() {
        @java.lang.Override
        public ModelFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new ModelFutureStub(channel, callOptions);
        }
      };
    return ModelFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void runModel(com.jason.mlsvconnx.proto.ModelRequest request,
        io.grpc.stub.StreamObserver<com.jason.mlsvconnx.proto.ModelReply> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getRunModelMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service Model.
   */
  public static abstract class ModelImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return ModelGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service Model.
   */
  public static final class ModelStub
      extends io.grpc.stub.AbstractAsyncStub<ModelStub> {
    private ModelStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ModelStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ModelStub(channel, callOptions);
    }

    /**
     */
    public void runModel(com.jason.mlsvconnx.proto.ModelRequest request,
        io.grpc.stub.StreamObserver<com.jason.mlsvconnx.proto.ModelReply> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getRunModelMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service Model.
   */
  public static final class ModelBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<ModelBlockingStub> {
    private ModelBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ModelBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ModelBlockingStub(channel, callOptions);
    }

    /**
     */
    public com.jason.mlsvconnx.proto.ModelReply runModel(com.jason.mlsvconnx.proto.ModelRequest request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getRunModelMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service Model.
   */
  public static final class ModelFutureStub
      extends io.grpc.stub.AbstractFutureStub<ModelFutureStub> {
    private ModelFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ModelFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new ModelFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<com.jason.mlsvconnx.proto.ModelReply> runModel(
        com.jason.mlsvconnx.proto.ModelRequest request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getRunModelMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_RUN_MODEL = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_RUN_MODEL:
          serviceImpl.runModel((com.jason.mlsvconnx.proto.ModelRequest) request,
              (io.grpc.stub.StreamObserver<com.jason.mlsvconnx.proto.ModelReply>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getRunModelMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              com.jason.mlsvconnx.proto.ModelRequest,
              com.jason.mlsvconnx.proto.ModelReply>(
                service, METHODID_RUN_MODEL)))
        .build();
  }

  private static abstract class ModelBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ModelBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return com.jason.mlsvconnx.proto.ModelOuterClass.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Model");
    }
  }

  private static final class ModelFileDescriptorSupplier
      extends ModelBaseDescriptorSupplier {
    ModelFileDescriptorSupplier() {}
  }

  private static final class ModelMethodDescriptorSupplier
      extends ModelBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    ModelMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (ModelGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ModelFileDescriptorSupplier())
              .addMethod(getRunModelMethod())
              .build();
        }
      }
    }
    return result;
  }
}
