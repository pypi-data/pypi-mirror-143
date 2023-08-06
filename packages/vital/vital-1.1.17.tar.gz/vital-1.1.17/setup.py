# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vital', 'vital.api', 'vital.internal']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.0.1,<3.0.0',
 'arrow',
 'auth0-python',
 'importlib-metadata>=3.7.3,<4.0.0',
 'requests',
 'svix>=0.41.2,<0.42.0']

setup_kwargs = {
    'name': 'vital',
    'version': '1.1.17',
    'description': '',
    'long_description': '# vital-python\n\nThe official Python Library for [Vital API](https://docs.tryvital.io)\n\n# Install\n\n```\npip install vital\n```\n\n# Calling Endpoints\n\n```\nfrom vital import Client\n\n# Available environments are \'sandbox\', \'development\', and \'production\'.\nclient = Client(client_id=\'***\', secret=\'***\', environment=\'sandbox\')\n```\n\n# Supported Endpoints\n\n```\n<!-- Dates have to be url encoded -->\nstart_date =  (datetime.now()-timedelta(days=1)).isoformat())\nend_date = datetime.now().isoformat()\n\nclient.Link.create(user_id="user_id")\nclient.Body.get(user_id=**,start_date, end_date)\nclient.Activity.get(user_id=**,start_date, end_date)\nclient.Sleep.get(user_id=**,start_date, end_date)\nclient.User.create(client_user_id=**)\nclient.User.providers(user_id=**)\nclient.User.get(client_user_id=**)\n\n\nfrom vital.types import WebhookEventCodes, WebhookType\n\nclient.Webhooks.test(WebhookEventCodes.HISTORICAL_DATA_UPDATE,\n                     WebhookType.ACTIVITY)\n```\n\n# Installing locally\n\n```\npoetry build --format sdist\ntar -xvf dist/*-`poetry version -s`.tar.gz -O \'*/setup.py\' > setup.py\n```\n',
    'author': 'maitham',
    'author_email': 'maitham@tryvital.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adeptlabs/vital-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
