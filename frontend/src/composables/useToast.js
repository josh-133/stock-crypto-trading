import { useToastStore } from '../stores/toast'

/**
 * Composable for easy toast notifications
 * Usage:
 *   const toast = useToast()
 *   toast.success('Trade executed!')
 *   toast.error('Something went wrong')
 */
export function useToast() {
  const store = useToastStore()

  return {
    success: (message, duration) => store.success(message, duration),
    error: (message, duration) => store.error(message, duration),
    warning: (message, duration) => store.warning(message, duration),
    info: (message, duration) => store.info(message, duration),
    dismiss: (id) => store.removeToast(id),
  }
}
