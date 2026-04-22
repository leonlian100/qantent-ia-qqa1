def get_patents(query):
    return [
        {"title": f"{query} device", "abstract": f"{query} cutting system using motor"},
        {"title": f"{query} machine", "abstract": f"automatic {query} with sensor"},
        {"title": f"{query} tool", "abstract": f"{query} blade rotation control"},
        {"title": f"{query} system", "abstract": f"{query} automatic feeding mechanism"},
        {"title": f"{query} innovation", "abstract": f"{query} smart control device"}
    ]
