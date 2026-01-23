export function useHeader(emit) {
  const handleLogout = () => {
    emit('logout');
  };

  return {
    handleLogout
  };
}
