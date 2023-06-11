<template>
  <DataTable
    :tableData="tableData"
    :totalItems="totalItmes"
    :columns="columns"
    @insert="handleInsert"
    :loading="!!loading"
    @delete="handleDelete"
    @update="handleUpdate"
    @refresh="handleRefresh"
    :allowEdit="allowEdit"
  />
</template>

<script>
import DataTable from "@/components/DataTable";
import {
  getProductList,
  insertProduct,
  deleteProducts,
  updateProduct,
} from "@/api/product";
import columns from "./columns";
import dayjs from "dayjs";
import { subscribe } from "@/utils/auth";

export default {
  components: {
    DataTable,
  },
  data() {
    return {
      tableData: [],
      columns,
      loading: 0,
      totalItmes: 0,
      pagination: {},
      allowEdit: false,
      sortInfo: null,
      searchObj: null,
    };
  },
  methods: {
    async handleRefresh(pagination, sortInfo, searchObj) {
      this.loading++;
      if (searchObj) {
        if (
          searchObj.date instanceof Array &&
          searchObj.date[0] &&
          searchObj.date[1]
        )
          searchObj = {
            ...searchObj,
            date: searchObj.date.map((item) =>
              dayjs(item).format("YYYY-MM-DD")
            ),
          };
        else
          searchObj = {
            ...searchObj,
            date: null,
          };

        searchObj = {
          ...searchObj,
          price: searchObj.price
            ? searchObj.price.map((item) => (item ? Number(item) : null))
            : null,
        };
      }

      const res = await getProductList(pagination, sortInfo, searchObj);
      this.pagination = pagination;
      this.searchObj = searchObj;
      this.sortInfo = sortInfo;
      this.tableData = res.list;
      this.totalItmes = res.total;
      this.loading--;
    },
    async handleInsert(data) {
      this.loading++;
      data.date = dayjs(data.date).format("YYYY-MM-DD");
      await insertProduct(data);
      this.handleRefresh(this.pagination, this.sortInfo, this.searchObj);
      this.loading--;
    },
    async handleDelete(list) {
      this.loading++;
      await deleteProducts(list);
      this.handleRefresh(this.pagination, this.sortInfo, this.searchObj);
      this.loading--;
    },
    async handleUpdate(data) {
      this.loading++;
      data.date = dayjs(data.date).format("YYYY-MM-DD");
      await updateProduct(data);
      this.handleRefresh(this.pagination, this.sortInfo, this.searchObj);
      this.loading--;
    },
  },
  created() {
    const that = this;
    subscribe((val) => {
      that.allowEdit = !!val;
    });
  },
};
</script>

<style>
</style>