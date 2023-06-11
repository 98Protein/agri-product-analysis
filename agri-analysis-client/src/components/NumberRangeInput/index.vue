<template>
  <div style="display: flex">
    <el-input
      style="flex: auto"
      v-model="value[0]"
      @input="v => $emit('input', [v, value[1]])"
      clearable
    />
    <span style="flex: none; margin: 0 10px">-</span>
    <el-input
      style="flex: auto"
      v-model="value[1]"
      @input="v => $emit('input', [value[0], v])"
      clearable
    />
  </div>
</template>

<script>
export default {
  props: {
    value: Array,
  },
  watch: {
    value(val) {
      if (!val)
        this.$emit('input', [null, null])
    }
  }
};
</script>

<style>
</style>