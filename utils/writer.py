from torch.utils.tensorboard import SummaryWriter
import torch.distributed as dist


def reduce_mean(tensor, nprocs):
    rt = tensor.clone()
    dist.all_reduce(rt, op=dist.ReduceOp.SUM)
    rt /= nprocs
    return rt


class Writer():
    def __init__(self, path):
        self.sw = SummaryWriter(path)
        self.dict = {}
        self.cnt = 0

    def init(self, dict={}):
        self.dict = dict
        self.cnt = 0

    def add_info(self, size, dict={}):
        for key in dict:
            self.dict[key] = (self.dict[key]*self.cnt + dict[key]*size)/(self.cnt+size)
        self.cnt += size

    def update(self, epoch):
        for key in self.dict:
            self.sw.add_scalar(key, self.dict[key], epoch)
        self.sw.flush()