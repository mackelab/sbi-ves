<template>
  <div class="g-edit-wrapper row">
    <div class="full-width" :class="justifyCenter">
      <div ref="stickyEditHeaderRef" class="row sticky-edit-header">
        <div class="col-12 col-xl-10 q-px-lg">
          <div class="row">
            <slot name="header"/>
          </div>
        </div>
      </div>
      <div class="row">
        <div :class="props.gridCss">
          <slot name="default"/>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">

const props = withDefaults(
  defineProps<{
    justifyCenter?: string | undefined;
    gridCss?: string | undefined;
  }>(),
  {
    gridCss: 'col-8 col-xl-8 q-px-lg',
    justifyCenter: '',
  }
);

import {onMounted, ref} from "vue";


const stickyEditHeaderRef = ref<HTMLDivElement | null>(null);

const stickyEditHeaderHeight = ref(0);

function getOuterHeight(element: HTMLElement) {
  const height = element.offsetHeight,
    style: CSSStyleDeclaration = window.getComputedStyle(element);

  return ['top', 'bottom']
    .map((side) => parseInt(<string>style[`margin-${side}` as keyof CSSStyleDeclaration]))
    .reduce((total, side) => total + side, height);
}

onMounted(() => {
  if (stickyEditHeaderRef.value) {
    const resizeObserver = new ResizeObserver(() => {
      if (stickyEditHeaderRef.value) {
        stickyEditHeaderHeight.value = getOuterHeight(stickyEditHeaderRef.value);
      }
    });
    resizeObserver.observe(stickyEditHeaderRef.value);
  }
})
</script>
<style scoped>

</style>
