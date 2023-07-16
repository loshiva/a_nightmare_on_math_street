from pwn import *
import re

def aggiusta_operazioni(richiesta: str) -> str:
    """Organizzo le operazioni dando le priorità giuste"""
    aggiusta_operazione = []
    dpo = False
    for unit in richiesta.split():
        if unit == "*":
            if dpo:
                aggiusta_operazione[-1] = f"{aggiusta_operazione[-1]}) *"
                dpo = False
            else:
                aggiusta_operazione.append(unit)
            continue

        if unit == "+":
            # Controllo se il pressimo pezzo contiene "("
            if richiesta[richiesta.index(unit)+1].startswith("("):
                aggiusta_operazione.append(unit)
                continue
            if dpo:
                aggiusta_operazione[-1] = f"{aggiusta_operazione[-1]} +"
            else:
                aggiusta_operazione[-1] = f"({aggiusta_operazione[-1]} +"
                dpo = True
            continue

        aggiusta_operazione.append(unit)

    if dpo:
        aggiusta_operazione[-1] += ")"

    aggiusta_operazione_str = " ".join(aggiusta_operazione)
    print(f"{aggiusta_operazione_str=}")
    return aggiusta_operazione_str

def risolvi_quesito():
    """Risolvo l'operazione e la invio alla macchina"""
    richiesta_str = conn.recvuntil("?", timeout=1).decode()
    print(f"{richiesta_str=}")
    richiesta = re.findall(r"\[\d+\]:\s+(.*?)\s+\=", richiesta_str)[0]
    print(f"{richiesta=}")
    aggiusta_operazione = aggiusta_operazioni(richiesta)
    risposta = str(eval(aggiusta_operazione))
    print(f"{risposta=}")

    conn.sendline(risposta)
    print("\n---\n")
    if "[500]" in richiesta_str:
        print(conn.recvline_contains("HTB", timeout=1).decode())
        exit(0)

global conn
conn = remote('159.65.81.48', 32672)

while 1:
    try:
        risolvi_quesito()
    except EOFError:
        print("EOFError...")
        break
