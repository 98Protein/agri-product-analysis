import Cookies from 'js-cookie';
import { getUserInfo as remoteGetUserInfo } from '@/api/admin'

let userInfo = null

const subscribeFuns = []

export function subscribe(fun) {
  subscribeFuns.push(fun)
  fun(userInfo)
}

export function getToken() {
  return Cookies.get('token');
}

export async function setToken(token) {
  Cookies.set('token', token, { expires: 1 });
  await getUserInfo()
  subscribeFuns.forEach(fun => fun(userInfo))
}

export function logout() {
  Cookies.remove('token')
  userInfo = null
  subscribeFuns.forEach(fun => fun(userInfo))
}

export async function getUserInfo() {
  if (!getToken())
    return null;
  if (userInfo) return userInfo
  userInfo = await remoteGetUserInfo()
  subscribeFuns.forEach(fun => fun(userInfo))
  return userInfo
}