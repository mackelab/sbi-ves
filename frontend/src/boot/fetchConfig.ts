import {boot} from 'quasar/wrappers';
import {useCoreStore} from 'stores/core';

export default boot(async () => {
  const coreStore = useCoreStore();

  if (coreStore.isLoggedIn) {
    coreStore.apiSetup();
  }
});
