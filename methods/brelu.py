import torch
import torch.nn as nn
from torch.autograd import Function


class brelu(Function):

    @staticmethod
    def forward(ctx, input):
        ctx.save_for_backward(input)

        input_shape = input.shape[0]
        even_indices = [i for i in range(0, input_shape, 2)]
        odd_indices = [i for i in range(1, input_shape, 2)]

        output = input.clone()

        output[even_indices] = output[even_indices].clamp(min=0)
        output[odd_indices] = output[odd_indices].clamp(max=0)

        return output

    @staticmethod
    def backward(ctx, grad_output):
        grad_input = None
        input, = ctx.saved_tensors

        if ctx.needs_input_grad[0]:
            grad_input = grad_output.clone()

        input_shape = input.shape[0]
        even_indices = [i for i in range(0, input_shape, 2)]
        odd_indices = [i for i in range(1, input_shape, 2)]

        grad_input[even_indices] = (input[even_indices] >= 0).float() * grad_input[even_indices]
        grad_input[odd_indices] = (input[odd_indices] < 0).float() * grad_input[odd_indices]

        return grad_input

class Classify(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 2)
        self.a1 = brelu.apply

    def forward(self, x):
        x = self.a1(self.fc1(x))
        return x

if __name__=='__main__':
    inputs = torch.randn(2,4)
    model = Classify()
    print(model(inputs))