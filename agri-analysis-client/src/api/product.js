import request from '@/utils/request';

export async function getProductList(pagination, sortInfo, searchObj) {
  const { data } = await request({
    method: 'post',
    url: `/api/product`,
    data: {
      pagination,
      sortInfo,
      searchObj
    }
  });
  return data;
}

export async function insertProduct(data) {
  await request({
    method: 'put',
    url: '/api/product',
    data
  })
}

export async function deleteProducts(list) {
  await request({
    method: 'delete',
    url: '/api/product',
    data: list
  })
}

export async function updateProduct(data) {
  await request({
    method: 'patch',
    url: '/api/product',
    data
  })
}