import streamlit as st
import time
import graphviz

# ---------------- Node Class ----------------
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# ---------------- BST Class ----------------
class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        return root

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Node with only one child or no child
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # Node with two children: get inorder successor
            temp = self.minValueNode(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        return root

    def minValueNode(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.key)
            self.inorder(root.right, result)

    def preorder(self, root, result):
        if root:
            result.append(root.key)
            self.preorder(root.left, result)
            self.preorder(root.right, result)

    def postorder(self, root, result):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.key)

    def search(self, root, key, path):
        if not root:
            return None
        path.append(root.key)
        if root.key == key:
            return root
        elif key < root.key:
            return self.search(root.left, key, path)
        else:
            return self.search(root.right, key, path)

# ---------------- Graphviz Draw ----------------
def draw_tree(root, highlight_nodes=None, highlight_color="green"):
    dot = graphviz.Digraph()
    highlight_nodes = highlight_nodes or []

    def add_nodes_edges(node):
        if node:
            if node.key in highlight_nodes:
                dot.node(str(node.key), style="filled", color=highlight_color, fillcolor=highlight_color)
            else:
                dot.node(str(node.key))
            if node.left:
                dot.edge(str(node.key), str(node.left.key))
                add_nodes_edges(node.left)
            if node.right:
                dot.edge(str(node.key), str(node.right.key))
                add_nodes_edges(node.right)
    add_nodes_edges(root)
    return dot

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="BST Visualizer", page_icon="🌳", layout="wide")

st.title("🌳 Advanced Binary Search Tree Visualizer")
st.write("Insert values and see BST Operations with Animation")

# Session state
if "tree" not in st.session_state:
    st.session_state.tree = BST()
    st.session_state.root = None

# Input for insert
values = st.text_input("Enter initial values (comma separated)", "50,30,70,20,40,60,80")

# Build Tree fresh
st.session_state.tree = BST()
st.session_state.root = None
for v in values.split(","):
    try:
        st.session_state.root = st.session_state.tree.insert(st.session_state.root, int(v.strip()))
    except:
        pass

# Draw initial tree
st.graphviz_chart(draw_tree(st.session_state.root))

# Traversal choice
option = st.selectbox("Choose Traversal", ["Inorder", "Preorder", "Postorder"])

if st.button("Run Traversal"):
    result = []
    if option == "Inorder":
        st.session_state.tree.inorder(st.session_state.root, result)
    elif option == "Preorder":
        st.session_state.tree.preorder(st.session_state.root, result)
    else:
        st.session_state.tree.postorder(st.session_state.root, result)

    placeholder = st.empty()
    traversal_path = ""
    for val in result:
        traversal_path += f"➡️ {val} "
        placeholder.markdown(f"**Traversal Progress:** {traversal_path}")
        st.graphviz_chart(draw_tree(st.session_state.root, [val], "yellow"))
        time.sleep(1)

    st.success(f"✅ {option} Traversal Done: {result}")

# Search
st.subheader("🔍 Search Node")
search_val = st.number_input("Enter value to search", value=40, step=1)
if st.button("Search"):
    path = []
    found = st.session_state.tree.search(st.session_state.root, search_val, path)
    for node in path:
        st.graphviz_chart(draw_tree(st.session_state.root, [node], "orange"))
        time.sleep(1)
    if found:
        st.success(f"✅ Value {search_val} found!")
        st.graphviz_chart(draw_tree(st.session_state.root, [search_val], "green"))
    else:
        st.error(f"❌ Value {search_val} not found!")

# Delete
st.subheader("❌ Delete Node")
delete_val = st.number_input("Enter value to delete", value=30, step=1)
if st.button("Delete"):
    st.session_state.root = st.session_state.tree.delete(st.session_state.root, delete_val)
    st.warning(f"Deleted {delete_val}")
    st.graphviz_chart(draw_tree(st.session_state.root))
