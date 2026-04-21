import useSettingsStore from '@/store/modules/settings'
import { DEFAULT_SYSTEM_TITLE } from '@/utils/systemTitle'

/**
 * 动态修改标题
 */
export function useDynamicTitle() {
  const settingsStore = useSettingsStore()
  const appTitle = settingsStore.appTitle || DEFAULT_SYSTEM_TITLE
  if (settingsStore.dynamicTitle) {
    document.title = settingsStore.title ? `${settingsStore.title} - ${appTitle}` : appTitle
  } else {
    document.title = appTitle
  }
}
