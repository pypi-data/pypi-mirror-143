# ecom-candidate-matching


## Getting started

```

# install packages
make install-dev

# run autolinting before pushing to git
make autolint

# run cleanup for hanging objects,etc
make clean

```

## System design

### Brief system overview

Suggest a 3 layer system, namely:
1. Feature enrichment requester type functions - to define how to retrieve or update feature enrichment layer i.e. any feature enrichment storage, caching and logging.
2. Scorer type functions - to define the steps to get a score i.e. any scoring based caching and tracking.
3. Business logic layer type workflow - to decide when scoring and feature enrichment happen and in which order. i.e. step functions.

This will allow separation of concerns and simplified functions. In the case of, waiting of dependencies or queueing the business layer will take care of this.

The overall system can be seen in the below diagram:

![event driven solution workflow](images/event_driven_inference_pipeline.png)

## Inference: Scoring backend layer

The set of scoring algorithms that can be selected, and used by client business logic. These should built to run independently as tasks, but could have data dependencies like 3rd party api data. Ultimately, we want to be able to track requests and results and monitor and evaluate the performance in production.

### Simple Cosine similarity

Leveraging the `Jarvis` API, using the entity embeddings / vectors, compute a distance similarity score between any two entities i.e. listing-candidate, candidate-candidate, listing-listing. Ideally batch scoring should be possible which would be any of the 3 according to selected type.

note: 
    - by design we should create a single function that provides all exhaustive match types for a scorer-type
    - expect each match type will be satisfied by a single request
    - each scorer-type should have it's own function, since "processing steps" will be specific for each scorer.
    - however, a scorer type could be multiple algos that share the same processing steps i.e. consine-sim or euclidean distance, etc.

An example payload could be:

```
# payload1 (from request)

{algo: 'cosine-sim', type: 'listing-candidate', item: [10001, 10002], items2: [899, 900, 999]}, # assuming the right are candidates, the left are listings

# payload 2 (from request)
{algo: 'cosine-sim', type: 'listing-listing', item: [10001, 10002], items2: [899, 900, 999]} # assuming the right are listings, the left are listings

# response 1
{
    status: success,
    type: 'listing-candidate',
    algo: 'cosine-sim',
    results: [
        {
            entity: 10001,
            entity_type: listing,
            scores: [0.2, 0.6, 0.1],
            match_entity_type: candidates
            matched_entities: [899, 900, 999],
            created_at: CURRENT_DATE
        },
        {
            entity: 10002,
            entity_type: listing,
            scores: [0.8, 0.6, 0.1],
            match_entity_type: candidates
            matched_entities: [899, 900, 999],
            created_at: CURRENT_DATE  # ofcourse this could be set to an SLA of hourly as well.
        }
    ]
}

```

## Inference: Request to 3rd party API backend

The set or collection of data enrichment systems, which leverage 3rd party API's. Ultimately, to keep the system performant caching or storage of enriched features should be possible and updateable.

### Jarvis

Jarvis system comprises two functionalities of interest to us, namely:
1. Feature enrichment which takes unstructured data and returns vector embeddings which can be used in downstream decision making.
2. Scoring system which would serve to return a valuable score to understand the closeness of match. `(currently not very performant)

It will be utlized primarily as a feature enrichment stage, returning vector embeddings that can be used to do downstream scoring of candidates and listings, for their similarity.

The suggested implementation is:
- an event driven task that can either be called in batch or stream modes to get embeddings
- a backend storage system which store vector embeddings and other enriched metadata for downstream ml stages

## Inference: Stage Data in Feature store

Requirements:
- query data to tabular format for tabular models
- preprocessing tasks (geo-encoding)
- fast query lookup

## Training: Train a model

Requirements:
- Train model once a month (CRON job)
- query data to job runtime
- Sagemaker serverless training job
- Sagemaker Endpoint / deployment of model assets

## Training: Stage Data in Feature store

Requirements:
- query data to tabular format for tabular models
- preprocessing tasks (geo-encoding)

## References

- AWS Step functions python sdk | https://aws-step-functions-data-science-sdk.readthedocs.io/en/stable/readmelink.html#steps
- AWS Step functions list of available states / steps | https://docs.aws.amazon.com/step-functions/latest/dg/concepts-states.html
- print or display a Step functions workflow before creation | https://aws-step-functions-data-science-sdk.readthedocs.io/en/stable/readmelink.html#visualizing-a-workflow
- Async AWS Lambda functions with API gateway | https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-integration-async.html
- Async AWS Lambda functions and destinations example | https://www.youtube.com/watch?v=kj0wH1g3DpQ
- AWS Step functions python sdk pass parameters to workflow at "execute" time | https://aws-step-functions-data-science-sdk.readthedocs.io/en/stable/placeholders.html 
- AWS Step Functions python sdk attach to existing workflow in account | https://aws-step-functions-data-science-sdk.readthedocs.io/en/stable/workflow.html#stepfunctions.workflow.Workflow.attach
- InputPath and controlling inputs in to steps | https://dev.to/dashbird/how-to-filter-and-manipulate-aws-step-functions-input-and-output-data-1jm9
