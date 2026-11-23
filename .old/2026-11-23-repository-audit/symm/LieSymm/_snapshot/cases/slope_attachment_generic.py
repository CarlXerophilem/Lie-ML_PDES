"""Attachment closure: K,G>0, n=m-1, 1<=m<=4, m!=3.

All cells use h_t+(hu)_x=0, u_t+u*u_x+g*(h+B)_x=0 and
B_t+D_x(K*u**m-G*u**n*B_x)=0 on h,u,g>0. Disabled terms are
removed BEFORE prolongation and shell construction. See models.branch_model.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from case_support import case_cli

if __name__ == '__main__':
    case_cli('slope_attachment_generic')
