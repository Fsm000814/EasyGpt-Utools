import { createStore } from 'vuex';

/**
 * 创建一个Vuex store
 */
export default createStore({
    state: {
        /**
         * 是否折叠侧边栏
         */
        collapsed: false,
        /**
         * 当前选中的菜单路径
         */
        selectedMenu: '/',
    },
    mutations: {
        /**
         * 切换侧边栏状态
         * @param state - state对象
         */
        toggleSidebar(state) {
            state.collapsed = !state.collapsed;
        },
        /**
         * 设置当前选中的菜单
         * @param state - state对象
         * @param menu - 菜单路径
         */
        setSelectedMenu(state, menu) {
            state.selectedMenu = menu;
        },
    },
    actions: {
        /**
         * 切换侧边栏状态
         * @param commit - commit函数
         */
        toggleSidebar({ commit }) {
            commit('toggleSidebar');
        },
        /**
         * 设置当前选中的菜单
         * @param commit - commit函数
         * @param menu - 菜单路径
         */
        setSelectedMenu({ commit }, menu) {
            commit('setSelectedMenu', menu);
        },
    },
});