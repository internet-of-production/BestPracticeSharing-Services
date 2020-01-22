export PYTHONPATH="${PYTHONPATH}:/Users/stefanbraun/PycharmProjects/BestPracticeSharing-Services/DatabaseIO/"
export PYTHONPATH="${PYTHONPATH}:/Users/stefanbraun/PycharmProjects/BestPracticeSharing-Services/MicroserviceBackend/"
eval "$(conda shell.bash hook)"
conda activate conda-env/osx/
pkill python
screen -dmS Frontend python MicroserviceFrontend/Frontend.py
screen -dmS DataImport python MicroserviceBackend/DataImportService/DataImportService.py
screen -dmS Clustering python MicroserviceBackend/RecommendationService/ClusteringService/ClusteringService.py
screen -dmS Scheduler python MicroserviceBackend/SchedulerService/SchedulerService.py
#screen -dmS Voting python MicroserviceBackend/RecommendationService/VotingService/VotingService.py
