import mlflow


class FLModel(mlflow.pyfunc.PythonModel):

    def create_strategy(self, num_rounds: int):
        import flwr
        from flwr.server.strategy import FedAvg
        from flwr.server.client_proxy import ClientProxy
        from typing import List, Tuple, Union, Optional, Dict
        from flwr.common import FitRes, Scalar, Parameters, parameters_to_ndarrays
        import numpy as np
        class SaveModelStrategy(FedAvg):

            def aggregate_fit(
                    self,
                    server_round: int,
                    results: List[Tuple[ClientProxy, FitRes]],
                    failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
            ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:

                    # Call aggregate_fit from base class (FedAvg) to aggregate parameters and metrics
                    aggregated_parameters, aggregated_metrics = super().aggregate_fit(server_round, results, failures)

                    if aggregated_parameters is not None and server_round == num_rounds:
                        # Convert `Parameters` to `List[np.ndarray]`
                        aggregated_ndarrays: List[np.ndarray] = parameters_to_ndarrays(aggregated_parameters)

                        # Save aggregated_ndarrays
                        print(f"Saving round {server_round} aggregated_ndarrays...")
                        np.savez(f"results.npz", *aggregated_ndarrays)

                    return aggregated_parameters, aggregated_metrics

        return SaveModelStrategy(
            min_available_clients=1,
            min_fit_clients=1,
            min_evaluate_clients=1
        )

    def create_model(self):
        import tensorflow as tf
        model = tf.keras.applications.MobileNetV2((32, 32, 3), classes=10, weights=None)
        model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
        class PythonModelWrapper():
            def __init__(self, model):
                self.model = model
            def predict(self, context, model_input):
                return self.model.fit
            def fit(self, x_train,y_train, epochs=1, batch_size=32, steps_per_epoch=3):
                self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, steps_per_epoch=steps_per_epoch)
            def get_weights(self):
                return self.model.get_weights()
            def set_weight(self,parameters):
                return self.model.set_weights(parameters)
            def evaluate(self,x_test,y_test):
                return self.model.evaluate(x_test, y_test)
        return PythonModelWrapper(model=model)


model = FLModel()

import cloudpickle
with open('model.pk', 'wb') as f:
    cloudpickle.dump(model, f)

