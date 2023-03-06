import torchvision.transforms as tvs_trans

from openood.utils.config import Config

from .transform import Convert, interpolation_modes, normalization_dict


class BasePreprocessor():
    """For train dataset standard transformation."""
    def __init__(self, config: Config):
        self.pre_size = config.dataset.pre_size
        self.image_size = config.dataset.image_size
        self.interpolation = interpolation_modes[config.dataset.interpolation]
        normalization_type = config.dataset.normalization_type
        if normalization_type in normalization_dict.keys():
            self.mean = normalization_dict[normalization_type][0]
            self.std = normalization_dict[normalization_type][1]
        else:
            self.mean = [0.5, 0.5, 0.5]
            self.std = [0.5, 0.5, 0.5]

        self.transform = tvs_trans.Compose([
            Convert('RGB'),
            tvs_trans.Resize(self.pre_size, interpolation=self.interpolation),
            tvs_trans.CenterCrop(self.image_size),
            tvs_trans.RandomHorizontalFlip(),
            tvs_trans.RandomCrop(self.image_size, padding=4),
            tvs_trans.ToTensor(),
            tvs_trans.Normalize(mean=self.mean, std=self.std),
        ])

        if config.preprocessor.randaugment.enable:
            n = config.preprocessor.randaugment.n
            m = config.preprocessor.randaugment.m
            self.transform.transforms.insert(
                1,
                tvs_trans.RandAugment(num_ops=n,
                                      magnitude=m,
                                      interpolation=self.interpolation))

    def setup(self, **kwargs):
        pass

    def __call__(self, image):
        return self.transform(image)
