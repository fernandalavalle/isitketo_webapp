# IsItKeto Web App

[![Build Status](https://travis-ci.org/mtlynch/isitketo_webapp.svg?branch=master)](https://travis-ci.org/mtlynch/isitketo_webapp)
[![Coverage Status](https://coveralls.io/repos/github/mtlynch/isitketo_webapp/badge.svg?branch=master)](https://coveralls.io/github/mtlynch/isitketo_webapp?branch=master)


To run IsItKeto,

Install dev requirements
```bash
pip install dev_requirements.txt
```

Install Google Cloud SDK following instructions [here.](https://cloud.google.com/appengine/docs/standard/python/download)

Install the extra python components.
```bash
gcloud components install app-engine-python-extras
```

Add appengine to PYTHONPATH.
```bash
PYTHONPATH="${PYTHONPATH}:/path/to/google-cloud-sdk/platform/google_appengine"
```

Finally, run

```bash
 dev_appserver.py app/app.yaml
 ```



