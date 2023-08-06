__version__ = '1.5.0'

from .util import TraceMode, PriorInflation, InferenceEngine, InferenceNetwork, Optimizer, LearningRateScheduler, ObserveEmbedding, set_verbosity, set_device, seed
from .state import sample, observe, factor, tag
from .address_dictionary import AddressDictionary
from .model import Model, RemoteModel, ConditionalModel, ParallelModel
