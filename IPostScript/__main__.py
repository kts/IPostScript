from ipykernel.kernelapp import IPKernelApp
from .kernel import PostscriptKernel
IPKernelApp.launch_instance(kernel_class=PostscriptKernel)
