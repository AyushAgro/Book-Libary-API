import dotenv
import os
import warnings
import yaml

warnings.simplefilter(action='ignore', category=FutureWarning)

env_filename = dotenv.find_dotenv()


if not env_filename:
    env_filename = os.path.join(__file__.split('src')[0], '.env')

dotenv.load_dotenv(dotenv_path=env_filename)

config_filename = (os.sep).join(__file__.split(os.sep)[:-1] + [os.getenv('config_filename')])
env_run = os.getenv('env_run', 'dev')


with open(config_filename, 'r') as stream:
    config = yaml.safe_load(stream)

