# Machine Learning Zoomcamp Capstone

## Introduction

The organization [datatalks.club](https://datatalks.club) has provided an online course 
entitled [Machine Learning Zoomcamp](https://datatalks.club/courses/2021-winter-ml-zoomcamp.html)
to provide a practical introduction to machine learning. The course is based on the book 
[Machine Learning Bookcamp](https://www.manning.com/books/machine-learning-bookcamp) by 
[Alexey Grigorev](https://alexeygrigorev.com/).

This project was undertaken as a capstone project for the Machine Learning Zoomcamp course.

## Project description

The service implemented here produces predictions for house prices based on data collected on residential property
sales in Ames, Iowa from 2006 to 2010. The data was shared by Dean De Cock in his paper ["Ames, Iowa: Alternative to the 
Boston Housing Data as an End of Semester Regression Project"](http://jse.amstat.org/v19n3/decock.pdf). De Cock intended
for the data to be used in projects by students taking coursework in statistics and, as the title of the paper suggests,
is meant to replace the commonly used [Boston housing dataset](http://dx.doi.org/10.1016/0095-0696(78)90006-2).

The project uses this data to produce a model and implements a service to produce predictions of the sale price of
a house based on the features provided in the request itself.

Some files of interest:

- [notebook.ipynb](notebook.ipynb): The Jupyter notebook used to perform EDA. Also, captures work to select and tune the 
  estimator used to create the model.
- [train.py](train.py): Produces the model binary used by the service to perform predictions 
- [predict.py](predict.py): Implementation of the prediction service using [Flask](https://flask.palletsprojects.com/)
- [predict_client.py](predict_client.py): An example client used to request predictions
- [Pipfile](Pipfile): Defines the project dependencies
- [Procfile](Procfile): Used by [Heroku](https://heroku.com) to run the prediction service

## Getting started

This project requires [Docker](https://docs.docker.com/get-docker/) and optionally [`make`](https://www.gnu.org/software/make/).
`make` is available typically readily available in Linux and can be installed on other OSs using their respective toolsets:

- Mac: [Homebrew](https://brew.sh/) or [xcode](https://apps.apple.com/us/app/xcode/)
- Windows: [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) or [Chocolatey](https://chocolatey.org/)

The following assumes that you have `make` installed. However, `make` is simply a wrapper to ease execution of the commands
using Python or Docker, so please consult the [`Makefile`](Makefile) to see the underlying commands used to work with the project.

To build the Docker image for the product, run `make build`.

To run the prediction service, run `make run-service`.

To run a Python client that makes example requests to the service, run `make run-client-local` to make a request to a local
version of the prediction service or `make run-client-remote` if you'd like to make requests to the service running in 
[Heroku](https://heroku.com).

The data used to train the model is available in [`data`](data). However, it can be downloaded using `make data`.

Binary versions of the model are available in [`bin`](bin). However, they can be regenerated using `make bin`.

## Deployment

The prediction service is available at https://zoomcamp-capstone.herokuapp.com. It can be deployed using
`make heroku-deploy` and requires installation of the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). 
Authentication is required to run `make heroku-deploy`. To authenticate, use `make heroku-login` and you will be prompted
to authenticate using a web browser. However, deployment is not necessary for testing as the service is available
publicly (see the notes regarding `make run-client-remote` above for how to make a request). The file [`Procfile`](Procfile)
is included for Heroku's sake so it knows how to start the service (see the Heroku docs on 
[Procfile](https://devcenter.heroku.com/articles/procfile) for further detail).

## Usage example

The service is available at https://zoomcamp-capstone.herokuapp.com/predict. A request provides the non-target 
variables defined in the data (see the [data documentation](data/DataDocumentation.txt) for details). The response 
contains a predicted sales price value.

The [example client](predict_client.py) sends a request using one of the rows from the test data set. The following
is an example request and response made by the client.

### Request

```json
{
   "ms_subclass":20,
   "ms_zoning":"RL",
   "lot_area":9612,
   "street":"Pave",
   "alley":"NA",
   "lot_shape":"Reg",
   "land_contour":"Lvl",
   "utilities":"AllPub",
   "lot_config":"Inside",
   "land_slope":"Gtl",
   "neighborhood":"Somerst",
   "condition_1":"Feedr",
   "condition_2":"Norm",
   "bldg_type":"1Fam",
   "house_style":"1Story",
   "overall_qual":8,
   "overall_cond":5,
   "year_built":2008,
   "year_remod/add":2009,
   "roof_style":"Gable",
   "roof_matl":"CompShg",
   "exterior_1st":"VinylSd",
   "exterior_2nd":"VinylSd",
   "mas_vnr_type":"Stone",
   "mas_vnr_area":72.0,
   "exter_qual":"Gd",
   "exter_cond":"TA",
   "foundation":"PConc",
   "bsmt_qual":"Gd",
   "bsmt_cond":"TA",
   "bsmt_exposure":"No",
   "bsmtfin_type_1":"Unf",
   "bsmtfin_sf_1":0.0,
   "bsmtfin_type_2":"Unf",
   "bsmtfin_sf_2":0.0,
   "bsmt_unf_sf":1468.0,
   "total_bsmt_sf":1468.0,
   "heating":"GasA",
   "heating_qc":"Ex",
   "central_air":true,
   "electrical":"SBrkr",
   "1st_flr_sf":1468,
   "2nd_flr_sf":0,
   "low_qual_fin_sf":0,
   "gr_liv_area":1468,
   "bsmt_full_bath":0.0,
   "bsmt_half_bath":0.0,
   "full_bath":2,
   "half_bath":0,
   "bedroom_abvgr":3,
   "kitchen_abvgr":1,
   "kitchen_qual":"Gd",
   "totrms_abvgrd":6,
   "functional":"Typ",
   "fireplaces":1,
   "fireplace_qu":"Gd",
   "garage_type":"Attchd",
   "garage_finish":"Fin",
   "garage_cars":3.0,
   "garage_area":898.0,
   "garage_qual":"TA",
   "garage_cond":"TA",
   "paved_drive":true,
   "wood_deck_sf":210,
   "open_porch_sf":150,
   "enclosed_porch":0,
   "3ssn_porch":0,
   "screen_porch":0,
   "pool_area":0,
   "pool_qc":"NA",
   "fence":"NA",
   "misc_feature":"NA",
   "misc_val":0,
   "mo_sold":12,
   "yr_sold":2009,
   "sale_type":"New",
   "sale_condition":"Partial"
}
```

### Response

```json
{
   "price":239011.84
}
```

## Dependencies

The project uses [Pipenv](https://pipenv.pypa.io/) to manage its dependencies. When used outside of Docker, the 
dependencies can be installed via `pipenv install` and the environment can be used via `pipenv shell`. 
To view the dependencies, see [`Pipfile`](Pipfile).
