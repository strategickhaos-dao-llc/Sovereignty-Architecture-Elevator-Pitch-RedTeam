#!/usr/bin/env python3
import json, time, os, argparse, subprocess, base64
from datetime import timedelta

def b64u(b): return base64.urlsafe_b64encode(b).rstrip(b'=')

def parse_ttl(s):
    if s.endswith('h'): return int(float(s[:-1]) * 3600)
    if s.endswith('m'): return int(float(s[:-1]) * 60)
    if s.endswith('d'): return int(float(s[:-1]) * 86400)
    return int(s)

parser = argparse.ArgumentParser()
parser.add_argument("--ca")
parser.add_argument("--yubi", type=int)
parser.add_argument("--node", required=True)
parser.add_argument("--cap", required=True)
parser.add_argument("--aud", required=True)
parser.add_argument("--ttl", default="86400")
args = parser.parse_args()

node_id = os.path.basename(args.node)
now = int(time.time())
exp = now + parse_ttl(args.ttl)
claims = {
  "iss":"SwarmCA","sub":node_id,"aud":args.aud,"iat":now,"exp":exp,
  "cap": [c.strip() for c in args.cap.split(",")],
  "jti": base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
}
header = {"alg":"EdDSA","typ":"JWT"}
pl = b'.'.join([b64u(json.dumps(header).encode()), b64u(json.dumps(claims).encode())])

if args.yubi:
    sig = subprocess.check_output(["yubihsm-eddsa-sign","--id","1"], input=pl)
else:
    # sign with age key using age-plugin mini-jws (simple ed25519); replace with your ed signer
    sk = open(args.ca,"rb").read()
    import nacl.signing, nacl.encoding, hashlib
    seed = sk.split(b'\n')[-2] if b'AGE-SECRET-KEY' in sk else hashlib.blake2b(sk, digest_size=32).digest()
    signing_key = nacl.signing.SigningKey(seed)
    sig = signing_key.sign(pl).signature

jwt = pl.decode()+"."+b64u(sig).decode()
open(os.path.join(args.node,"token.jwt"),"w").write(jwt)
print(jwt)
