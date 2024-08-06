import {RouteRecordRaw} from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'rootPublic',
    component: () => import('layouts/SecondaryLayout.vue'),
    children: [
      {
        path: '/login',
        name: 'login',
        component: () => import('pages/LoginPage.vue'),
        meta: {
          authorize: false,
        },
      },
      {
        path: '/logout',
        name: 'logout',
        component: () => import('pages/LogoutPage.vue'),
        meta: {
          authorize: false,
        },
      },
      {
        path: '/register',
        name: 'register',
        component: () => import('pages/RegisterPage.vue'),
        meta: {
          authorize: false,
        },
      }]
  },
  {
    path: '/',
    name: 'root',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '/', name: 'discover ', component: () => import('pages/IndexPage.vue')},
      {path: '/home', name: 'home', component: () => import('pages/IndexPage.vue')},
      {path: '/ping', name: 'ping', component: () => import ('pages/PingPage.vue')},
      {path: '/user', name: 'user', component: () => import ('pages/EditUser.vue')},
      {path: '/inversion', name: 'inversion', component: () => import ('pages/UploadMeasurements.vue')},
      {path: '/upload', name: 'upload', component: () => import ('pages/UploadMeasurements.vue')}
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
