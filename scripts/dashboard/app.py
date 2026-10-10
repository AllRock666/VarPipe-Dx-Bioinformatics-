import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="VarPipe-Dx Dashboard", layout="wide")

st.title("VarPipe-Dx Clinical Variant Dashboard")
st.markdown("Interactive multi-omics dashboard for variant interpretation.")

# Mock Data
st.header("1. Variant Classifications")
classification_data = pd.DataFrame({
    'Classification': ['Pathogenic', 'Likely Pathogenic', 'VUS', 'Likely Benign', 'Benign'],
    'Count': [12, 45, 120, 890, 4500]
})

col1, col2 = st.columns(2)

with col1:
    st.dataframe(classification_data, hide_index=True)

with col2:
    st.bar_chart(classification_data.set_index('Classification'))

# Volcano Plot (Mock)
st.header("2. RNA-seq Differential Expression (Volcano Plot)")

# Generate mock DE data
np.random.seed(42)
n_genes = 1000
log2fc = np.random.normal(0, 1.5, n_genes)
pvals = np.random.uniform(0, 1, n_genes)
padj = pvals * 10  # Mock correction
padj = np.clip(padj, 0, 1)
neg_log10_padj = -np.log10(padj + 1e-10)

de_df = pd.DataFrame({
    'Gene': [f"GENE_{i}" for i in range(n_genes)],
    'log2FoldChange': log2fc,
    'padj': padj,
    '-log10(padj)': neg_log10_padj
})

# Highlight significant
de_df['Significant'] = (de_df['padj'] < 0.05) & (de_df['log2FoldChange'].abs() > 1)

st.scatter_chart(
    de_df,
    x='log2FoldChange',
    y='-log10(padj)',
    color='Significant'
)

st.header("3. Multi-Omics Hits")
st.markdown("Genes with **Pathogenic Variants** AND **Significant Differential Expression**:")

multi_omics_hits = pd.DataFrame({
    'Gene': ['BRCA1', 'TP53'],
    'Variant': ['c.5266dupC', 'c.133T>A (VUS)'],
    'log2FoldChange': [-2.1, 0.5],
    'padj': [1.2e-4, 0.45]
})

st.table(multi_omics_hits)
