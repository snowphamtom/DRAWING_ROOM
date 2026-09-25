#!/usr/bin/env python3
"""MeetLM — Class C seed.

From-scratch character net. No pretrained weights. Not a product.
Two streams meet (q from A, k/v from B). A refuse head gates decode.
Train only on the house strings embedded below.

Default steps=60: measured elbow on this corpus (loss flattened by step 60–79).
Cosine LR + early-stop if 20-step delta < 0.03.

MAGPIE stays 19/658,750 pending. Theater stays paused.
"""
from __future__ import annotations

import argparse
import math
import sys

import torch
import torch.nn as nn

CORPUS = """
Admit only what fits.
claimed <= interior.
propose is not commit.
unknown is not available.
Denial is successful governance.
The room is a webpage, not a product.
Occupancy does not travel.
Star means interaction, not a new integer.
Theater stays paused.
Sourced figures only.
Receipt is not award.
""".strip()

BLOCK = 48
D = 48
LAYERS = 2
HEADS = 4
STEPS = 60
PATIENCE = 20
MIN_DELTA = 0.03


class MeetBlock(nn.Module):
    def __init__(self, d: int, n_head: int) -> None:
        super().__init__()
        self.ln_a = nn.LayerNorm(d)
        self.ln_b = nn.LayerNorm(d)
        self.q = nn.Linear(d, d, bias=False)
        self.k = nn.Linear(d, d, bias=False)
        self.v = nn.Linear(d, d, bias=False)
        self.proj = nn.Linear(d, d, bias=False)
        self.ff = nn.Sequential(
            nn.LayerNorm(d), nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d)
        )
        self.n_head = n_head

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, t, c = x.shape
        h = self.n_head
        dh = c // h
        q = self.q(self.ln_a(x)).view(b, t, h, dh).transpose(1, 2)
        k = self.k(self.ln_b(x)).view(b, t, h, dh).transpose(1, 2)
        v = self.v(self.ln_b(x)).view(b, t, h, dh).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(dh)
        mask = torch.tril(torch.ones(t, t, device=x.device))
        att = att.masked_fill(mask == 0, float("-inf"))
        att = torch.softmax(att, dim=-1)
        meet = (att @ v).transpose(1, 2).contiguous().view(b, t, c)
        x = x + self.proj(meet)
        return x + self.ff(x)


class MeetLM(nn.Module):
    def __init__(self, vocab: int) -> None:
        super().__init__()
        self.tok = nn.Embedding(vocab, D)
        self.pos = nn.Embedding(BLOCK, D)
        self.blocks = nn.ModuleList([MeetBlock(D, HEADS) for _ in range(LAYERS)])
        self.ln = nn.LayerNorm(D)
        self.head = nn.Linear(D, vocab, bias=False)
        self.admit = nn.Linear(D, 1)
        self.head.weight = self.tok.weight

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None):
        b, t = idx.shape
        x = self.tok(idx) + self.pos(torch.arange(t, device=idx.device))
        for blk in self.blocks:
            x = blk(x)
        x = self.ln(x)
        logits = self.head(x)
        admit = torch.sigmoid(self.admit(x)).squeeze(-1)
        loss = None
        if targets is not None:
            ce = nn.functional.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
            gate = nn.functional.binary_cross_entropy(admit, (targets != 0).float())
            loss = ce + 0.2 * gate
        return logits, admit, loss


def main() -> int:
    p = argparse.ArgumentParser(description="MeetLM Class C seed")
    p.add_argument("--steps", type=int, default=STEPS)
    p.add_argument("--prompt", default="Admit only")
    p.add_argument("--no-early-stop", action="store_true")
    args = p.parse_args()

    chars = sorted(set(CORPUS))
    stoi = {c: i for i, c in enumerate(chars)}
    itos = {i: c for c, i in stoi.items()}
    data = torch.tensor([stoi[c] for c in CORPUS], dtype=torch.long)
    torch.manual_seed(371)
    m = MeetLM(len(chars))
    opt = torch.optim.AdamW(m.parameters(), lr=4e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=max(args.steps, 1))
    nparam = sum(p.numel() for p in m.parameters())
    print(f"params={nparam} vocab={len(chars)} tokens={len(data)} class=C steps_cap={args.steps}")

    def batch(bs: int = 8):
        ix = torch.randint(0, len(data) - BLOCK - 1, (bs,))
        x = torch.stack([data[i : i + BLOCK] for i in ix])
        y = torch.stack([data[i + 1 : i + BLOCK + 1] for i in ix])
        return x, y

    last_mark = None
    stopped = args.steps
    for step in range(args.steps):
        x, y = batch()
        _, _, loss = m(x, y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        val = float(loss.detach())
        if step % 20 == 0 or step == args.steps - 1:
            print(f"step {step} loss {val:.4f} lr {sched.get_last_lr()[0]:.5f}")
            if (
                not args.no_early_stop
                and last_mark is not None
                and abs(last_mark - val) < MIN_DELTA
                and step >= PATIENCE
            ):
                print(f"early_stop at {step} delta={abs(last_mark-val):.4f}")
                stopped = step + 1
                break
            last_mark = val

    print(f"used_steps={stopped}")
    m.eval()
    idx = torch.tensor([[stoi[c] for c in args.prompt if c in stoi]], dtype=torch.long)
    refused = 0
    with torch.no_grad():
        for _ in range(60):
            ctx = idx[:, -BLOCK:]
            logits, admit, _ = m(ctx)
            if float(admit[0, -1].detach()) < 0.35:
                refused += 1
                nxt = torch.tensor([[stoi.get(" ", 0)]])
            else:
                nxt = torch.multinomial(torch.softmax(logits[:, -1] / 0.8, dim=-1), 1)
            idx = torch.cat([idx, nxt], 1)
    text = "".join(itos[int(i)] for i in idx[0])
    print("sample:", text)
    print("refused_steps:", refused)
    print("not a product. MAGPIE 19/658,750 pending.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
