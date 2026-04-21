import { getNormalPath } from '@/utils/ruoyi'
import { isExternal } from '@/utils/validate'

export const DEFAULT_FALLBACK_ROUTE = '/user/profile'

export function getFirstAccessibleRoute(routes = [], fallback = DEFAULT_FALLBACK_ROUTE) {
  return findFirstRoute(routes) || fallback
}

export function hasAccessibleRoute(routes = [], path) {
  const normalizedPath = getNormalPath(path)
  return Boolean(findRouteByPath(routes, normalizedPath))
}

function findFirstRoute(routes = [], basePath = '') {
  for (const route of routes) {
    if (shouldSkipRoute(route)) {
      continue
    }

    const routePath = resolveRoutePath(basePath, route.path)
    if (route.children && route.children.length) {
      const childPath = findFirstRoute(route.children, routePath)
      if (childPath) {
        return childPath
      }
    }

    if (isNavigableRoute(route, routePath)) {
      return routePath
    }
  }
  return ''
}

function findRouteByPath(routes = [], targetPath, basePath = '') {
  for (const route of routes) {
    if (shouldSkipRoute(route)) {
      continue
    }

    const routePath = resolveRoutePath(basePath, route.path)
    if (isNavigableRoute(route, routePath) && routePath === targetPath) {
      return route
    }

    if (route.children && route.children.length) {
      const childRoute = findRouteByPath(route.children, targetPath, routePath)
      if (childRoute) {
        return childRoute
      }
    }
  }
  return null
}

function shouldSkipRoute(route) {
  return !route || route.hidden || isExternal(route.path || '')
}

function isNavigableRoute(route, routePath) {
  return routePath && routePath !== '/' && route.redirect !== 'noRedirect' && route.path !== '*'
}

function resolveRoutePath(basePath, routePath = '') {
  if (!routePath) {
    return getNormalPath(basePath || '/')
  }
  if (routePath.startsWith('/')) {
    return getNormalPath(routePath)
  }
  return getNormalPath(`${basePath}/${routePath}`)
}
