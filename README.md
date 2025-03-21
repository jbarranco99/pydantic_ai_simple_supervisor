# LangGraph Multi-Agent Supervisor (Pydantic Replica)

This project is a **replica of LangGraph's Supervisor basic example**, but implemented using **Pydantic AI**. It demonstrates a hierarchical multi-agent system where a **supervisor agent** orchestrates **specialized agents** (such as a **math agent** and a **research agent**) to handle different types of tasks efficiently.

## Features

**Supervisor Agent** to manage task delegation  
**Math Agent** for structured mathematical calculations  
**Research Agent** for retrieving external data  
**Tool-based agent handoff** for seamless communication  
**Message history management** for context tracking  
**Pydantic for structured outputs**  

---

## Example Usage

```plaintext
### ** 1 User Query (Math Task)**
User: "What is 5 * 3 + 2?"

### **2 User Query (Research Task)**
User: "Whats the employee number of FAANG companies?"

### ** 3 User Query (Combined Task)**
User: "Whats the combined number of FAANG employees?"
```

## 🔗 References

**LangGraph Supervisor:** https://github.com/langchain-ai/langgraph-supervisor-py  
**Pydantic AI:** https://ai.pydantic.dev



