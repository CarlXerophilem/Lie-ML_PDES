"""Isotropic 2D SVE branch: slope_attachment_generic_f0.

h_t+div(h*w)=0; w_t+(w.grad)w+g*grad(h+B)+f*J*w=0;
B_t+div(K*|w|**(m-1)*w-G*|w|**n*grad(B))=0.
The shared model registry removes disabled terms before jet construction.
Continuous exponents remain symbolic; h>0 and |w|>0.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from case_support_2d import case_cli

if __name__=='__main__':
    case_cli('slope_attachment_generic_f0')
