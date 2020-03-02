export PYTHONPATH="${PYTHONPATH}:/Users/stefanbraun/PycharmProjects/BestPracticeSharing-Services/DatabaseIO/"
export PYTHONPATH="${PYTHONPATH}:/Users/stefanbraun/PycharmProjects/BestPracticeSharing-Services/MicroserviceBackend/"
eval "$(conda shell.bash hook)"
conda activate conda-env/osx/
pkill python
screen -dmS MicroserviceFrontend python MicroserviceFrontend/MicroserviceFrontend.py
screen -dmS DataImport python Backend/DataImportService/DataImportService.py
screen -dmS Clustering python Backend/RecommendationService/ClusteringService/ClusteringService.py
screen -dmS Scheduler python Backend/SchedulerService/SchedulerService.py
#screen -dmS Voting python Backend/RecommendationService/VotingService/VotingService.py
