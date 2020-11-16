import numpy as np
import torch.nn as nn

from timm.models.helpers import build_model_with_cfg
from timm.models.layers import ConvBnAct, SEModule


def _mcfg(**kwargs):
    cfg = dict()
    cfg.update(**kwargs)
    return cfg


# Model FLOPS = three trailing digits * 10^8
model_cfgs = dict(
    regnetx_002=_mcfg(w0=24, wa=36.44, wm=2.49, group_w=8, depth=13, se_ratio=0.0),
    regnetx_004=_mcfg(w0=24, wa=24.48, wm=2.54, group_w=16, depth=22, se_ratio=0.0),
    regnetx_006=_mcfg(w0=48, wa=36.97, wm=2.24, group_w=24, depth=16, se_ratio=0.0),
    regnetx_008=_mcfg(w0=56, wa=35.73, wm=2.28, group_w=16, depth=16, se_ratio=0.0),
    regnetx_016=_mcfg(w0=80, wa=34.01, wm=2.25, group_w=24, depth=18, se_ratio=0.0),
    regnetx_032=_mcfg(w0=88, wa=26.31, wm=2.25, group_w=48, depth=25, se_ratio=0.0),
    regnetx_040=_mcfg(w0=96, wa=38.65, wm=2.43, group_w=40, depth=23, se_ratio=0.0),
    regnetx_064=_mcfg(w0=184, wa=60.83, wm=2.07, group_w=56, depth=17, se_ratio=0.0),
    regnetx_080=_mcfg(w0=80, wa=49.56, wm=2.88, group_w=120, depth=23, se_ratio=0.0),
    regnetx_120=_mcfg(w0=168, wa=73.36, wm=2.37, group_w=112, depth=19, se_ratio=0.0),
    regnetx_160=_mcfg(w0=216, wa=55.59, wm=2.1, group_w=128, depth=22, se_ratio=0.0),
    regnetx_320=_mcfg(w0=320, wa=69.86, wm=2.0, group_w=168, depth=23, se_ratio=0.0),

    regnety_002=_mcfg(w0=24, wa=36.44, wm=2.49, group_w=8, depth=13, se_ratio=0.25),
    regnety_004=_mcfg(w0=48, wa=27.89, wm=2.09, group_w=8, depth=16, se_ratio=0.25),
    regnety_006=_mcfg(w0=48, wa=32.54, wm=2.32, group_w=16, depth=15, se_ratio=0.25),
    regnety_008=_mcfg(w0=56, wa=38.84, wm=2.4, group_w=16, depth=14, se_ratio=0.25),
    regnety_016=_mcfg(w0=48, wa=20.71, wm=2.65, group_w=24, depth=27, se_ratio=0.25),
    regnety_032=_mcfg(w0=80, wa=42.63, wm=2.66, group_w=24, depth=21, se_ratio=0.25),
    regnety_040=_mcfg(w0=96, wa=31.41, wm=2.24, group_w=64, depth=22, se_ratio=0.25),
    regnety_064=_mcfg(w0=112, wa=33.22, wm=2.27, group_w=72, depth=25, se_ratio=0.25),
    regnety_080=_mcfg(w0=192, wa=76.82, wm=2.19, group_w=56, depth=17, se_ratio=0.25),
    regnety_120=_mcfg(w0=168, wa=73.36, wm=2.37, group_w=112, depth=19, se_ratio=0.25),
    regnety_160=_mcfg(w0=200, wa=106.23, wm=2.48, group_w=112, depth=18, se_ratio=0.25),
    regnety_320=_mcfg(w0=232, wa=115.89, wm=2.53, group_w=232, depth=20, se_ratio=0.25),
)


def _cfg(url=''):
    return {
        'url': url,
    }


default_cfgs = dict(
    regnetx_002=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_002-e7e85e5c.pth'),
    regnetx_004=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_004-7d0e9424.pth'),
    regnetx_006=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_006-85ec1baa.pth'),
    regnetx_008=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_008-d8b470eb.pth'),
    regnetx_016=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_016-65ca972a.pth'),
    regnetx_032=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_032-ed0c7f7e.pth'),
    regnetx_040=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_040-73c2a654.pth'),
    regnetx_064=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_064-29278baa.pth'),
    regnetx_080=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_080-7c7fcab1.pth'),
    regnetx_120=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_120-65d5521e.pth'),
    regnetx_160=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_160-c98c4112.pth'),
    regnetx_320=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnetx_320-8ea38b93.pth'),
    regnety_002=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_002-e68ca334.pth'),
    regnety_004=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_004-0db870e6.pth'),
    regnety_006=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_006-c67e57ec.pth'),
    regnety_008=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_008-dc900dbe.pth'),
    regnety_016=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_016-54367f74.pth'),
    regnety_032=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/regnety_032_ra-7f2439f9.pth'),
    regnety_040=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_040-f0d569f9.pth'),
    regnety_064=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_064-0a48325c.pth'),
    regnety_080=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_080-e7f3eb93.pth'),
    regnety_120=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_120-721ba79a.pth'),
    regnety_160=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_160-d64013cd.pth'),
    regnety_320=_cfg(url='https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-regnet/regnety_320-ba464b29.pth'),
)


def quantize_float(f, q):
    """Converts a float to closest non-zero int divisible by q."""
    return int(round(f / q) * q)


def adjust_widths_groups_comp(widths, groups):
    """Adjusts the compatibility of widths and groups."""
    groups = [min(g, w_bot) for g, w_bot in zip(groups, widths)]
    widths = [quantize_float(w_bot, g) for w_bot, g in zip(widths, groups)]
    return widths, groups


def generate_regnet(width_slope, width_initial, width_mult, depth, q=8):
    """Generates per block widths from RegNet parameters."""
    assert width_slope >= 0 and width_initial > 0 and width_mult > 1 and width_initial % q == 0
    widths_cont = np.arange(depth) * width_slope + width_initial
    width_exps = np.round(np.log(widths_cont / width_initial) / np.log(width_mult))
    widths = width_initial * np.power(width_mult, width_exps)
    widths = np.round(np.divide(widths, q)) * q
    num_stages, max_stage = len(np.unique(widths)), width_exps.max() + 1
    widths, widths_cont = widths.astype(int).tolist(), widths_cont.tolist()
    return widths, num_stages, max_stage, widths_cont


class Bottleneck(nn.Module):
    """ RegNet Bottleneck

    This is almost exactly the same as a ResNet Bottlneck. The main difference is the SE block is moved from
    after conv3 to after conv2. Otherwise, it's just redefining the arguments for groups/bottleneck channels.
    """

    def __init__(self,
                 in_channels,
                 out_channels,
                 stride=1,
                 bottleneck_factor=1,
                 group_width=1,
                 se_ratio=0.0):
        super(Bottleneck, self).__init__()
        self.use_se = (se_ratio > 0.0)
        assert (bottleneck_factor == 1)

        mid_channels = out_channels // bottleneck_factor
        groups = mid_channels // group_width

        self.conv1 = ConvBnAct(
            in_channels,
            mid_channels,
            kernel_size=1)
        self.conv2 = ConvBnAct(
            mid_channels,
            mid_channels,
            kernel_size=3,
            stride=stride,
            dilation=1,
            groups=groups)
        if self.use_se:
            self.se = SEModule(
                mid_channels,
                reduction_channels=int(round(in_channels * se_ratio)))
        self.conv3 = ConvBnAct(
            mid_channels,
            out_channels,
            kernel_size=1,
            act_layer=None)
        self.act3 = nn.ReLU(inplace=True)

        if (in_channels != out_channels) or (stride != 1):
            self.downsample = ConvBnAct(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=1,
                stride=stride,
                dilation=1,
                norm_layer=nn.BatchNorm2d,
                act_layer=None)
        else:
            self.downsample = None

    def forward(self, x):
        shortcut = x
        x = self.conv1(x)
        x = self.conv2(x)
        if self.use_se:
            x = self.se(x)
        x = self.conv3(x)
        if self.downsample is not None:
            shortcut = self.downsample(shortcut)
        x += shortcut
        x = self.act3(x)
        return x


class RegStage(nn.Module):
    """Stage (sequence of blocks w/ the same output shape)."""

    def __init__(self,
                 in_channels,
                 out_channels,
                 depth,
                 group_width,
                 se_ratio):
        super(RegStage, self).__init__()
        for i in range(depth):
            stride = 2 if i == 0 else 1
            block_in_chs = in_channels if i == 0 else out_channels

            self.add_module(
                name="b{}".format(i + 1), module=Bottleneck(
                    in_channels=block_in_chs,
                    out_channels=out_channels,
                    stride=stride,
                    group_width=group_width,
                    se_ratio=se_ratio)
            )

    def forward(self, x):
        for block in self.children():
            x = block(x)
        return x


class RegNet(nn.Module):
    """RegNet model.

    Paper: https://arxiv.org/abs/2003.13678
    Original Impl: https://github.com/facebookresearch/pycls/blob/master/pycls/models/regnet.py
    """
    def __init__(self,
                 cfg,
                 in_channels=3,
                 in_size=(224, 224),
                 num_classes=1000):
        super().__init__()
        self.in_size = in_size
        self.num_classes = num_classes

        self.features = nn.Sequential()

        stem_width = 32

        # Construct the stem
        self.features.add_module("stem", ConvBnAct(
            in_channels=in_channels,
            out_channels=stem_width,
            kernel_size=3,
            stride=2))

        # Construct the stages
        in_channels = stem_width
        stage_params = self._get_stage_params(cfg)
        se_ratio = cfg['se_ratio']
        for i, stage_args in enumerate(stage_params):
            stage_name = "s{}".format(i + 1)
            self.features.add_module(stage_name, RegStage(
                in_channels=in_channels,
                **stage_args,
                se_ratio=se_ratio))
            in_channels = stage_args['out_channels']

        self.features.add_module("global_pool", nn.AdaptiveAvgPool2d(output_size=1))
        self.fc = nn.Linear(
            in_features=in_channels,
            out_features=num_classes,
            bias=True)
        pass

    def _get_stage_params(self,
                          cfg):
        # Generate RegNet ws per block
        w_a, w_0, w_m, d = cfg['wa'], cfg['w0'], cfg['wm'], cfg['depth']
        widths, num_stages, _, _ = generate_regnet(w_a, w_0, w_m, d)

        # Convert to per stage format
        stage_widths, stage_depths = np.unique(widths, return_counts=True)

        # Use the same group width, bottleneck mult and stride for each stage
        stage_groups = [cfg['group_w'] for _ in range(num_stages)]

        # Adjust the compatibility of ws and gws
        stage_widths, stage_groups = adjust_widths_groups_comp(stage_widths, stage_groups)
        param_names = ['out_channels', 'depth', 'group_width']
        stage_params = [
            dict(zip(param_names, params)) for params in
            zip(stage_widths, stage_depths, stage_groups)]
        return stage_params

    def forward(self, x):
        x = self.features(x)
        x = x.flatten(1)
        x = self.fc(x)
        return x


def _create_regnet(variant, pretrained, **kwargs):
    return build_model_with_cfg(
        model_cls=RegNet,
        variant=variant,
        pretrained=pretrained,
        default_cfg=default_cfgs[variant],
        model_cfg=model_cfgs[variant],
        **kwargs)


def regnetx_002(pretrained=False, **kwargs):
    """RegNetX-200MF"""
    return _create_regnet('regnetx_002', pretrained, **kwargs)


def regnetx_004(pretrained=False, **kwargs):
    """RegNetX-400MF"""
    return _create_regnet('regnetx_004', pretrained, **kwargs)


def regnetx_006(pretrained=False, **kwargs):
    """RegNetX-600MF"""
    return _create_regnet('regnetx_006', pretrained, **kwargs)


def regnetx_008(pretrained=False, **kwargs):
    """RegNetX-800MF"""
    return _create_regnet('regnetx_008', pretrained, **kwargs)


def regnetx_016(pretrained=False, **kwargs):
    """RegNetX-1.6GF"""
    return _create_regnet('regnetx_016', pretrained, **kwargs)


def regnetx_032(pretrained=False, **kwargs):
    """RegNetX-3.2GF"""
    return _create_regnet('regnetx_032', pretrained, **kwargs)


def regnetx_040(pretrained=False, **kwargs):
    """RegNetX-4.0GF"""
    return _create_regnet('regnetx_040', pretrained, **kwargs)


def regnetx_064(pretrained=False, **kwargs):
    """RegNetX-6.4GF"""
    return _create_regnet('regnetx_064', pretrained, **kwargs)


def regnetx_080(pretrained=False, **kwargs):
    """RegNetX-8.0GF"""
    return _create_regnet('regnetx_080', pretrained, **kwargs)


def regnetx_120(pretrained=False, **kwargs):
    """RegNetX-12GF"""
    return _create_regnet('regnetx_120', pretrained, **kwargs)


def regnetx_160(pretrained=False, **kwargs):
    """RegNetX-16GF"""
    return _create_regnet('regnetx_160', pretrained, **kwargs)


def regnetx_320(pretrained=False, **kwargs):
    """RegNetX-32GF"""
    return _create_regnet('regnetx_320', pretrained, **kwargs)


def regnety_002(pretrained=False, **kwargs):
    """RegNetY-200MF"""
    return _create_regnet('regnety_002', pretrained, **kwargs)


def regnety_004(pretrained=False, **kwargs):
    """RegNetY-400MF"""
    return _create_regnet('regnety_004', pretrained, **kwargs)


def regnety_006(pretrained=False, **kwargs):
    """RegNetY-600MF"""
    return _create_regnet('regnety_006', pretrained, **kwargs)


def regnety_008(pretrained=False, **kwargs):
    """RegNetY-800MF"""
    return _create_regnet('regnety_008', pretrained, **kwargs)


def regnety_016(pretrained=False, **kwargs):
    """RegNetY-1.6GF"""
    return _create_regnet('regnety_016', pretrained, **kwargs)


def regnety_032(pretrained=False, **kwargs):
    """RegNetY-3.2GF"""
    return _create_regnet('regnety_032', pretrained, **kwargs)


def regnety_040(pretrained=False, **kwargs):
    """RegNetY-4.0GF"""
    return _create_regnet('regnety_040', pretrained, **kwargs)


def regnety_064(pretrained=False, **kwargs):
    """RegNetY-6.4GF"""
    return _create_regnet('regnety_064', pretrained, **kwargs)


def regnety_080(pretrained=False, **kwargs):
    """RegNetY-8.0GF"""
    return _create_regnet('regnety_080', pretrained, **kwargs)


def regnety_120(pretrained=False, **kwargs):
    """RegNetY-12GF"""
    return _create_regnet('regnety_120', pretrained, **kwargs)


def regnety_160(pretrained=False, **kwargs):
    """RegNetY-16GF"""
    return _create_regnet('regnety_160', pretrained, **kwargs)


def regnety_320(pretrained=False, **kwargs):
    """RegNetY-32GF"""
    return _create_regnet('regnety_320', pretrained, **kwargs)


def _calc_width(net):
    import numpy as np
    net_params = filter(lambda p: p.requires_grad, net.parameters())
    weight_count = 0
    for param in net_params:
        weight_count += np.prod(param.size())
    return weight_count


def _test():
    import torch

    pretrained = False

    models = [
        regnetx_002,
        regnetx_004,
        regnetx_006,
        regnetx_008,
        regnetx_016,
        regnetx_032,
        regnetx_040,
        regnetx_064,
        regnetx_080,
        regnetx_120,
        regnetx_160,
        regnetx_320,

        regnety_002,
        regnety_004,
        regnety_006,
        regnety_008,
        regnety_016,
        regnety_032,
        regnety_040,
        regnety_064,
        regnety_080,
        regnety_120,
        regnety_160,
        regnety_320,
    ]

    for model in models:

        net = model(pretrained=pretrained)

        # net.train()
        net.eval()
        weight_count = _calc_width(net)
        print("m={}, {}".format(model.__name__, weight_count))
        assert (model != regnetx_002 or weight_count == 2684792)
        assert (model != regnetx_004 or weight_count == 5157512)
        assert (model != regnetx_006 or weight_count == 6196040)
        assert (model != regnetx_008 or weight_count == 7259656)
        assert (model != regnetx_016 or weight_count == 9190136)
        assert (model != regnetx_032 or weight_count == 15296552)
        assert (model != regnetx_040 or weight_count == 22118248)
        assert (model != regnetx_064 or weight_count == 26209256)
        assert (model != regnetx_080 or weight_count == 39572648)
        assert (model != regnetx_120 or weight_count == 46106056)
        assert (model != regnetx_160 or weight_count == 54278536)
        assert (model != regnetx_320 or weight_count == 107811560)

        assert (model != regnety_002 or weight_count == 3162996)
        assert (model != regnety_004 or weight_count == 4344144)
        assert (model != regnety_006 or weight_count == 6055160)
        assert (model != regnety_008 or weight_count == 6263168)
        assert (model != regnety_016 or weight_count == 11202430)
        assert (model != regnety_032 or weight_count == 19436338)
        assert (model != regnety_040 or weight_count == 20646656)
        assert (model != regnety_064 or weight_count == 30583252)
        assert (model != regnety_080 or weight_count == 39180068)
        assert (model != regnety_120 or weight_count == 51822544)
        assert (model != regnety_160 or weight_count == 83590140)
        assert (model != regnety_320 or weight_count == 145046770)

        x = torch.randn(1, 3, 224, 224)
        y = net(x)
        y.sum().backward()
        assert (tuple(y.size()) == (1, 1000))


if __name__ == "__main__":
    _test()
