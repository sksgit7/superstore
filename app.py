import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from PIL import Image

st.title('Store Performance Analysis')

#load dataset
@st.cache
def data():
	df=pd.read_excel('Week1-Superstore.xlsx',sheet_name='Superstore-Retail-Sep-2020')
	df['Shipdate'] =  pd.to_datetime(df['ShipDate'], format='%Y%b%d')
	df['year']=pd.DatetimeIndex(df['ShipDate']).year
	df['month']=pd.DatetimeIndex(df['ShipDate']).month
	df[df['year']!=2020]
	return df
df=data()

#checkbox to show data
if st.checkbox('View dataset'):
	if st.button('Full'):
		st.write(data())
	elif st.button('Head'):
		st.write(data().head())

year= st.sidebar.multiselect('Select year(s):',\
		(2016,2017,2018,2019))
category= st.sidebar.multiselect('Select category(s):',\
		['Furniture', 'Office Supplies', 'Technology'])

if st.checkbox('Sales-Profit trend'):
	st.markdown('<center>Avg. Sales per month</center>', unsafe_allow_html=True)
		
	if year==[] and category==[]:
		st.line_chart(data().groupby('month')['Sales'].sum())
	
	else:
		def plot1(df):
			group1=df.groupby(['year','month'])['Sales'].sum().reset_index()
			fig, ax= plt.subplots(figsize=(6,3))
			ax=sns.lineplot(data=group1, x='month', y='Sales', hue='year')
			ax.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
			ax.set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
			st.pyplot(fig)
		if category==[]:
			df=data()[data()['year'].isin(year)]
			plot1(df)

		elif year and category:
			df=data()[data()['year'].isin(year) & data()['Category'].isin(category)]
			plot1(df)
		else:
			df= data()[data()['Category'].isin(category)]
			plot1(df)


if year:
	df=data()[data()['year'].isin(year)]
	if category:
		df=df[df['Category'].isin(category)]
	elif category:
		df=data()[data()['Category'].isin(category)]
	else:
		df=data()


if st.checkbox('Profit margin'):
	
	st.header(str(round(df['Profit'].sum()/df['Sales'].sum()*100,2))+ '%')
	if len(year)>1 or len(category)>1:
		st.write('Note: Data is avg. of multi-fields chosen')

if st.checkbox('Sales-Profit-Discount%'):
	fig, ax= plt.subplots(figsize=(4,2))
	sns.lineplot(data=df.groupby(['Category'])['Sales'].mean().reset_index(), x='Category', y='Sales', ax=ax, label='Sales', marker='o')
	sns.lineplot(data=df.groupby(['Category'])['Profit'].mean().reset_index(), x='Category', y='Profit', ax=ax, label='Profit', marker='o')
	ax2=ax.twinx()
	sns.barplot(data=df.groupby(['Category'])['DiscountPercent'].mean().reset_index(), x='Category', y='DiscountPercent', ax=ax2, label='Discount', 
	            linewidth=.5, facecolor=(0, 0, 0, 0.1),edgecolor=".2")
	st.pyplot(fig)

if st.checkbox('Region analysis'):
	f1=st.multiselect('Select fields',['Sales','Profit'])
	if f1:
		for x in f1:
			d1=df.groupby('Region')[x].mean()
			if x=='Sales':
				fig, ax= plt.subplots(figsize=(1,1))
				plt.rcParams.update({'font.size': 7})
				ax=plt.pie(d1.values, labels= d1.index, autopct='%.1f')
				st.pyplot(fig)
				plt.rcParams.update({'font.size': 10})

			else:
				fig,ax= plt.subplots(figsize=(4,2))
				ax=sns.barplot(d1.index, d1.values)
				st.pyplot(fig)

if st.checkbox('Category analysis'):
	f2=st.multiselect('Select fields',['Sales','Profit'])
	if f2:
		for x in f2:
			d1=df.groupby('Category')[x].mean()
			if x=='Sales':
				fig, ax= plt.subplots(figsize=(1,1))
				plt.rcParams.update({'font.size': 7})
				ax=plt.pie(d1.values, labels= d1.index, autopct='%.1f')
				st.pyplot(fig)
				plt.rcParams.update({'font.size': 10})

			else:
				fig,ax= plt.subplots(figsize=(4,2))
				ax=sns.barplot(d1.index, d1.values)
				st.pyplot(fig)
	