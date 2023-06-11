<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-header-left" v-if="allowEdit">
        <el-button
          type="success"
          icon="el-icon-plus"
          size="medium"
          @click="insertDlgVisible = true"
          :disabled="editingIndex != null"
        >
          添加
        </el-button>
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="medium"
          :disabled="selection.length == 0 || editingIndex != null"
          @click="handleDeleteMany"
        >
          删除
        </el-button>
      </div>
      <div class="page-header-right">
        <el-button
          icon="el-icon-search"
          @click="handleStartSearch"
          :disabled="editingIndex != null"
          :style="searching ? {color: 'red'} : null"
        >
          搜索
        </el-button>
      </div>
    </div>

    <div class="page-main">
      <el-table
        :data="currentData"
        :height="tableHeight"
        v-loading="loading"
        @selection-change="(val) => (selection = val)"
        @sort-change="handleSortChanged"
      >
        <el-table-column type="selection" width="30"> </el-table-column>
        <template v-for="column in columns">
          // index
          <el-table-column
            v-if="column.type === 'index'"
            :key="column.key || column.prop || column.title"
            type="index"
            width="50"
            align="right"
            label="#"
          />

          // date
          <el-table-column
            v-if="column.type === 'date'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
            :sortable="!!column.sortable && 'custom'"
          >
            <template v-slot="scope">
              <span v-if="editingIndex !== scope.$index || !column.editable">
                {{ dayjs(scope.row[column.prop]).format(column.format) }}
              </span>
              <el-date-picker
                v-else
                v-model="editingObj[column.prop]"
                type="date"
                placeholder="选择日期"
              />
            </template>
          </el-table-column>

          // text
          <el-table-column
            v-if="column.type === 'text'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
            :sortable="!!column.sortable && 'custom'"
          >
            <template v-slot="scope">
              <span v-if="editingIndex !== scope.$index || !column.editable">
                {{ scope.row[column.prop] }}
              </span>
              <el-input v-else v-model="editingObj[column.prop]" />
            </template>
          </el-table-column>

          // cascade
          <el-table-column
            v-if="column.type === 'cascade'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
            :sortable="!!column.sortable && 'custom'"
          >
            <template v-slot="scope">
              <span v-if="editingIndex !== scope.$index || !column.editable">
                {{
                  column.formatFuns[column.degree - 1](scope.row[column.prop])
                    .title
                }}
              </span>
              <el-cascader
                v-else
                :value="column.getValuesFun(editingObj[column.prop])"
                @change="
                  (v) =>
                    column.handleChangeFun(editingObj, v[column.degree - 1])
                "
                :props="{
                  lazy: true,
                  lazyLoad(node, resolve) {
                    column.getOptionsFuns[node.level](node.value).then((res) =>
                      resolve(res)
                    );
                  },
                }"
              />
            </template>
          </el-table-column>

          // number
          <el-table-column
            v-if="column.type === 'number'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
            :sortable="!!column.sortable && 'custom'"
          >
            <template v-slot="scope">
              <span v-if="editingIndex !== scope.$index || !column.editable">
                {{ scope.row[column.prop] }} {{ column.suffix }}
              </span>
              <span v-else>
                <el-input-number
                  style="margin-right: 5px"
                  v-model="editingObj[column.prop]"
                  :precision="column.precision"
                  :step="column.step"
                />
                {{ column.suffix }}
              </span>
            </template>
          </el-table-column>

          // options
          <el-table-column
            v-if="column.type === 'select'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
          >
            <template v-slot="scope">
              <span v-if="editingIndex !== scope.$index || !column.editable">
                {{
                  column.options.find(
                    (option) => option.value === scope.row[column.prop]
                  ).title
                }}
              </span>
              <el-select
                v-else
                v-model="editingObj[column.prop]"
                placeholder="请选择"
              >
                <el-option
                  v-for="option in column.options"
                  :key="option.value"
                  :label="option.title"
                  :value="option.value"
                >
                </el-option>
              </el-select>
            </template>
          </el-table-column>

          // operations
          <el-table-column
            v-if="column.type === 'operations' && allowEdit"
            :key="column.key || column.prop || column.title"
            :label="column.title"
            :width="250"
          >
            <template v-slot="scope">
              <el-button
                v-if="editingIndex !== scope.$index"
                :disabled="editingIndex !== null"
                size="small"
                type="primary"
                icon="el-icon-edit"
                @click="handleStartEdit(scope.$index, scope.row)"
              >
                编辑
              </el-button>
              <template v-else>
                <el-button
                  size="small"
                  type="primary"
                  icon="el-icon-check"
                  @click="handleConfirmEdit"
                >
                  确定
                </el-button>
                <el-button
                  @click="handleCancelEdit"
                  size="small"
                  icon="el-icon-close"
                >
                  取消
                </el-button>
              </template>

              <el-button
                v-if="editingIndex !== scope.$index"
                :disabled="editingIndex !== null"
                size="small"
                type="danger"
                icon="el-icon-delete"
                @click="handleDeleteOne(scope.row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </template>
      </el-table>
    </div>

    <el-dialog title="新增" :visible.sync="insertDlgVisible">
      <el-form :model="insertObj" label-width="80px">
        <template v-for="column in columns">
          <el-form-item
            :key="column.key || column.prop || column.title"
            :label="column.title"
            v-if="column.type === 'text'"
          >
            <el-input v-model="insertObj[column.prop]" />
          </el-form-item>

          <el-form-item
            :key="column.key || column.prop || column.title"
            :label="column.title"
            v-else-if="column.type === 'date'"
          >
            <el-date-picker v-model="insertObj[column.prop]" />
          </el-form-item>

          <el-form-item
            :key="column.key || column.prop || column.title"
            :label="column.title"
            v-if="column.type === 'number'"
          >
            <el-input-number
              style="margin-right: 10px"
              :precision="column.precision"
              :step="column.step"
              v-model="insertObj[column.prop]"
            />
            {{ column.suffix }}
          </el-form-item>

          <el-form-item
            v-if="column.type === 'select'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
          >
            <el-select v-model="insertObj[column.prop]" placeholder="请选择">
              <el-option
                v-for="option in column.options"
                :key="option.value"
                :label="option.title"
                :value="option.value"
              >
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item
            v-if="column.type === 'cascade'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
          >
            <el-cascader
              :value="column.getValuesFun(insertObj[column.prop])"
              @change="
                (v) => column.handleChangeFun(insertObj, v[column.degree - 1])
              "
              :props="{
                lazy: true,
                lazyLoad(node, resolve) {
                  column.getOptionsFuns[node.level](node.value).then((res) =>
                    resolve(res)
                  );
                },
              }"
            />
          </el-form-item>
        </template>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleInsertCancel">取 消</el-button>
        <el-button type="primary" @click="handleInsertConfirm">
          确 定
        </el-button>
      </div>
    </el-dialog>

    <el-drawer
      title="高级搜索"
      :visible.sync="searchDrawerShow"
      direction="rtl"
    >
      <el-form
        label-position="right"
        label-width="80px"
        style="margin-right: 30px"
      >
        <template v-for="column in columns">
          <el-form-item
            :key="column.key || column.prop || column.title"
            :label="column.title"
            v-if="column.type === 'text'"
          >
            <el-input v-model="searchObj[column.prop]" clearable />
          </el-form-item>
          <el-form-item
            :key="column.key || column.prop || column.title"
            :label="column.title"
            v-else-if="column.type === 'date'"
          >
            <el-date-picker
              v-model="searchObj[column.prop]"
              clearable
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              :picker-options="pickerOptions"
            >
            </el-date-picker>
          </el-form-item>
          <el-form-item
            :key="column.key || column.prop || column.title"
            :label="column.title"
            v-if="column.type === 'number'"
          >
            <NumberRangeInput v-model="searchObj[column.prop]" />
          </el-form-item>

          <el-form-item
            v-if="column.type === 'cascade'"
            :key="column.key || column.prop || column.title"
            :label="column.title"
          >
            <el-cascader
              :value="column.getValuesFun(searchObj[column.prop])"
              @change="
                (v) => column.handleChangeFun(searchObj, v[column.degree - 1])
              "
              clearable
              :props="{
                lazy: true,
                lazyLoad(node, resolve) {
                  column.getOptionsFuns[node.level](node.value).then((res) =>
                    resolve(res)
                  );
                },
              }"
            />
          </el-form-item>
        </template>
        <el-form-item>
          <el-button type="primary" @click="handleConfirmSearch">搜索</el-button>
          <el-button @click="searchDrawerShow = false">取消</el-button>
          <el-button style="float: right" @click="handleClearSearch">清空</el-button>
        </el-form-item>
      </el-form>
    </el-drawer>

    <div class="page-footer">
      <el-pagination
        class="page-footer-pagination"
        :current-page="pagination.pageNo"
        :page-sizes="[25, 50, 100, 200, 300, 400]"
        :page-size="pagination.pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
        @current-change="
          (currentPage) => handlePaginationChange({ pageNo: currentPage })
        "
        @size-change="
          (currentSize) => handlePaginationChange({ pageSize: currentSize })
        "
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import dayjs from "dayjs";
import NumberRangeInput from "@/components/NumberRangeInput";

export default {
  props: {
    tableData: Array,
    columns: Array,
    loading: Boolean,
    totalItems: Number,
    allowEdit: Boolean
  },
  components: {
    NumberRangeInput,
  },
  data() {
    return {
      dayjs,
      editingIndex: null,
      editingObj: {},
      pagination: {
        pageNo: 1,
        pageSize: 25,
        total: 0,
      },
      documentHeight: document.documentElement.clientHeight,
      selection: [],

      searchDrawerShow: false,
      searchObj: {},
      searching: false,
      currentData: [],

      insertDlgVisible: false,
      insertObj: {},

      sortInfo: null,

      pickerOptions: {
          shortcuts: [{
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit('pick', [start, end]);
            }
          }]
        },
    };
  },
  methods: {
    handleConfirmSearch() {
      this.searching = true
      this.$emit("refresh", this.pagination, this.sortInfo, this.searchObj);
      this.searchDrawerShow = false;
    },
    handleClearSearch() {
      this.searching = false;
      this.$emit("refresh", this.pagination, this.sortInfo, this.searchObj);
      this.searchObj = {}
    },
    handleSortChanged({column, order}) {
      this.sortInfo = {
        column: this.columns.find(item => item.title === column.label).prop,
        order
      }
      this.$emit("refresh", this.pagination, this.sortInfo, this.searchObj);
    },
    handleConfirmEdit() {
      for (let column of this.columns) {
        if (!column.nullable && !this.editingObj[column.prop])
          return this.$message.error(`${column.title}不能为空`)
      }
      this.$emit("update", this.editingObj);
      this.editingIndex = null;
      this.editingObj = {};
    },
    handleDeleteMany() {
      this.$confirm("此操作将删除所有选中项，是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() =>
        this.$emit(
          "delete",
          this.selection.map((item) => item.id)
        )
      );
    },
    handleDeleteOne(id) {
      this.$confirm("此操作将删除该项，是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => this.$emit("delete", [id]));
    },
    handleInsertCancel() {
      this.insertDlgVisible = false;
      this.insertObj = {};
    },
    async handleInsertConfirm() {
      for (let column of this.columns) {
        if (!column.nullable && !this.insertObj[column.prop])
          return this.$message.error(`${column.title}不能为空`)
      }
      this.$emit("insert", this.insertObj);
      this.insertDlgVisible = false;
      this.insertObj = {};
    },
    handleStartEdit(index, obj) {
      this.editingIndex = index;
      this.editingObj = { ...obj };
    },
    handleCancelEdit() {
      this.editingIndex = null;
      this.editingObj = {};
    },
    handleStartSearch() {
      this.searchDrawerShow = true;
    },
    handlePaginationChange(currentPagination) {
      this.pagination = {
        ...this.pagination,
        ...currentPagination,
      };
      this.$emit("refresh", this.pagination, this.sortInfo, this.searchObj);
    },
    getSearchInitObj() {
      const result = {};
      this.columns
        .filter((column) => column.searchable)
        .forEach((column) => {
          switch (column.type) {
            case "text":
              result[column.prop] = "";
              break;
            case "date":
              result[column.prop] = [null, null];
              break;
            case "number":
              result[column.prop] = [null, null];
              break;
            default:
              result[column.prop] = null;
              break;
          }
        });
      return result;
    },
  },
  mounted() {
    this.currentData = this.tableData;
    window.onresize = () =>
      (this.documentHeight = document.documentElement.clientHeight);
  },
  computed: {
    tableHeight() {
      return Math.max(this.documentHeight - 258, 400);
    },
  },
  created() {
    this.searchObj = this.getSearchInitObj();
    this.$emit("refresh", this.pagination);
  },
  watch: {
    tableData(val) {
      this.currentData = val;
      this.selection = [];
    },
    totalItems(val) {
      this.pagination = {
        ...this.pagination,
        total: val,
      };
    },
  },
};
</script>

<style scoped lang="scss">
.page-container {
  display: flex;
  flex-direction: column;

  .page-header {
    flex: none;
    margin-bottom: 10px;
    display: flex;
    .page-header-right {
      margin-left: auto;
    }
  }

  .page-main {
    flex: auto;
  }

  .page-footer {
    flex: none;
    display: flex;
    margin-top: 15px;

    .page-footer-pagination {
      margin-left: auto;
    }
  }
}
</style>