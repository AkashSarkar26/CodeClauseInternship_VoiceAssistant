def insertText(text_node, text):
  text_node.config(state='normal')
  text_node.insert('end', text)
  text_node.config(state="disabled")
