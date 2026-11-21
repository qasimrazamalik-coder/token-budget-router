#!/usr/bin/env python3
import argparse, json, re, sys

def context(d):
    budget=max(1,int(d.get("token_budget",1000))); used=0; selected=[]; excluded=[]
    items=sorted(d.get("items",[]), key=lambda x:(not x.get("required",False), -(float(x.get("relevance",0))*.55+float(x.get("freshness",0))*.2+float(x.get("trust",0))*.25)))
    for x in items:
        tokens=max(1,len(str(x.get("text","")))//4); item={"id":x.get("id"),"estimated_tokens":tokens}
        if used+tokens<=budget or x.get("required"):
            used+=tokens; selected.append(item|{"score":round(float(x.get("relevance",0))*.55+float(x.get("freshness",0))*.2+float(x.get("trust",0))*.25,3)})
        else: excluded.append(item|{"reason":"token_budget"})
    return {"task":d.get("task"),"budget":budget,"estimated_tokens":used,"selected":selected,"excluded":excluded}

def mcp(d):
    findings=[]
    for t in d.get("tools",[]):
        n=t.get("name","unnamed"); desc=t.get("description",""); scopes=set(t.get("scopes",[])); params=t.get("parameters",{})
        if scopes & {"admin","root","*"}: findings.append({"severity":"high","rule":"MCP-001","tool":n,"issue":"overbroad scope","fix":"replace administrative scope with minimum resource/action scope"})
        if t.get("side_effect") and not re.search(r"create|update|delete|send|write|purchase|deploy",desc,re.I): findings.append({"severity":"high","rule":"MCP-002","tool":n,"issue":"side effect is not explicit","fix":"state the external mutation and confirmation boundary"})
        if t.get("side_effect") and not params: findings.append({"severity":"medium","rule":"MCP-003","tool":n,"issue":"unconstrained mutation","fix":"define typed, bounded parameters and idempotency behavior"})
        if re.search(r"password|secret|token|api.?key",json.dumps(params),re.I): findings.append({"severity":"high","rule":"MCP-004","tool":n,"issue":"possible secret parameter","fix":"use managed credential references, never raw secrets"})
    return {"server":d.get("server"),"tools_audited":len(d.get("tools",[])),"findings":findings,"pass":not any(x["severity"]=="high" for x in findings)}

def router(d):
    c=float(d.get("complexity",0)); risk=d.get("risk","low"); privacy=d.get("privacy","public"); budget=int(d.get("token_budget",0))
    tier="frontier" if c>=.75 or risk=="high" else "balanced" if c>=.4 else "fast"
    if budget<2000 and tier=="frontier": tier="balanced-with-escalation"
    strategy="local-first" if privacy in {"restricted","confidential"} else "retrieval-first" if budget<8000 else "full-context"
    return {"model_tier":tier,"context_strategy":strategy,"max_iterations":2 if budget<4000 else 4,"escalate_if":["failed validation","high-impact ambiguity","tool permission expansion"]}

def regression(d):
    rows=[]
    for c in d.get("cases",[]):
        out=c.get("output",""); reasons=[]
        reasons += [f"missing term: {x}" for x in c.get("required_terms",[]) if x.lower() not in out.lower()]
        reasons += [f"forbidden term: {x}" for x in c.get("forbidden_terms",[]) if x.lower() in out.lower()]
        if len(out.split())>int(c.get("max_words",10**9)): reasons.append("word budget exceeded")
        reasons += [f"missing section: {x}" for x in c.get("required_sections",[]) if x.lower() not in out.lower()]
        rows.append({"id":c.get("id"),"pass":not reasons,"reasons":reasons})
    return {"cases":rows,"score":round(sum(x["pass"] for x in rows)/len(rows),3) if rows else 0}

def handoff(d):
    req=["task","owner","completed","evidence","assumptions","risks","next_action","authorization"]
    missing=[x for x in req if x not in d or d[x] in (None,"",[])]
    blockers=[]
    if missing: blockers.append({"rule":"HANDOFF-001","missing":missing})
    if d.get("authorization") not in {"read-only","prepare-only","execute-approved"}: blockers.append({"rule":"HANDOFF-002","issue":"authorization boundary is invalid"})
    return {"score":round((len(req)-len(missing))/len(req),3),"ready":not blockers,"blockers":blockers,"normalized":{k:d.get(k) for k in req}}

MODES={"context":context,"mcp":mcp,"router":router,"regression":regression,"handoff":handoff}
def main():
    p=argparse.ArgumentParser(); p.add_argument("input"); p.add_argument("--mode",required=True,choices=MODES); p.add_argument("--output")
    a=p.parse_args(); data=json.load(open(a.input,encoding="utf-8")); result=MODES[a.mode](data); text=json.dumps(result,indent=2)
    if a.output: open(a.output,"w",encoding="utf-8").write(text+"\n")
    else: print(text)
if __name__=="__main__": main()
