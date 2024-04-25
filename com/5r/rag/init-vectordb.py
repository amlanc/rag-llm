## Document Loader
import contextlib
import warnings
import os
import ssl
from urllib3.exceptions import InsecureRequestWarning
import nltk
from langchain.document_loaders import PyPDFDirectoryLoader

# Disable SSL certificate verification
old_merge_env_settings = requests.Session.merge_environment_settings

@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()
    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_env_settings(self, url, proxies, stream, verify, cert)
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_env_settings
        for adapter in opened_adapters:
            try:
                adapter.close()
            except Exception as e:
                print(f"Some thing happend \n{e}\n")


#ssl._create_default_https_context = no_ssl_verification()
#ssl._create_default_https_context = ssl._create_unverified_context
#ssl._create_default_https_context = ssl._create_unverified_context
with no_ssl_verification():
    print("SSL is disabled. Calling nltk download..")
    if os.path.isfile("/Users/amlanchatterjee/nltk_data/corpora/wordnet.zip") is None:
        nltk.download('wordnet')

    if os.path.isfile("/Users/amlanchatterjee/nltk_data/tokenizers/punkt.zip") is None:
        nltk.download('punkt')


PDF_FOLDER_PATH = "data"
loader = PyPDFDirectoryLoader(PDF_FOLDER_PATH)
raw_pdf_doc = loader.load()
print("PDF Loaded")
