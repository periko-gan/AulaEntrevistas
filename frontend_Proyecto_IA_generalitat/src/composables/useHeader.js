/**
 * @description Composable para gestionar la lógica del encabezado (Header).
 * @param {Function} emit - La función `emit` del componente para enviar eventos al padre.
 * @returns {object} Un objeto con todas las variables y funciones reactivas para el componente.
 */
export function useHeader(emit) {
  /**
   * @description Emite un evento 'logout' al componente padre.
   */
  const handleLogout = () => {
    emit('logout');
  };

  return {
    handleLogout
  };
}
