import request from '@/utils/request';

export async function getProvinceList() {
  const { data } = await request({
    method: 'get',
    url: '/api/province'
  });
  return data;
}

export async function getCityList(provinceId) {
  const { data } = await request({
    method: 'get',
    url: '/api/city?province=' + provinceId
  });
  return data;
}

export async function getMarketList(cityId) {
  const { data } = await request({
    method: 'get',
    url: '/api/market?city=' + cityId
  });
  return data;
}

export async function getMarket(marketId) {
  const { data } = await request({
    method: 'get',
    url: '/api/market/' + marketId
  });
  return data;
}

export async function getTypeList() {
  const { data } = await request({
    method: 'get',
    url: '/api/type'
  });
  return data;
}

export async function getVarietyList(typeId) {
  const { data } = await request({
    method: 'get',
    url: '/api/variety?type=' + typeId
  });
  return data;
}

export async function getVariety(varietyId) {
  const { data } = await request({
    method: 'get',
    url: '/api/variety/' + varietyId
  });
  return data;
}
