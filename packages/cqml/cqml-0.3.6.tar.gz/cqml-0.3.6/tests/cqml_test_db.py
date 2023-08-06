# Databricks notebook source
# MAGIC %md
# MAGIC # CQML
# MAGIC ## Compact Query Meta Language
# MAGIC ### Databricks Test Notebook

# COMMAND ----------

!pip install --upgrade pip
#!pip install cqml
#--IMPORT-CQML--#
!pip --no-cache-dir install git+https://github.com/TheSwanFactory/cqml.git@v36-super-saver
!pip install cqml==0.3.6.dev5
#++IMPORT-CQML++#

import cqml

# COMMAND ----------

KEY="cqml_test"
cvm = cqml.load_cqml(KEY,spark, '.')
cvm.debug = True
cvm.run()

# COMMAND ----------

#dict = cvm.do_save({})

# COMMAND ----------

#displayHTML(dict['html'])
#dict

# COMMAND ----------

#spark.sql('create database nauto')

# COMMAND ----------

#spark.sql('drop table if exists default.3g_devices_superfleet')
