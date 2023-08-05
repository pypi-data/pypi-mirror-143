(self.webpackChunkcodechecker=self.webpackChunkcodechecker||[]).push([[771],{20376:(e,t,n)=>{"use strict";n.d(t,{k:()=>o}),n(54678),n(91058);var r=n(96486),i=n.n(r);const o={bind:function(e,t){var n=t.value||function(){},r=t.options||{passive:!0},o=function(){var t=function(e){e.style.overflow="auto";var t=window.innerHeight,n=e.getBoundingClientRect().top,r=0,i=document.querySelector("footer");if(i){var o=window.getComputedStyle(i);r=parseFloat(o.height)}for(var s=e,a=null,c=0;s.parentNode&&s.parentNode!==document;)s=s.parentNode,a=window.getComputedStyle(s),c+=parseInt(a.paddingBottom,10);return e.style.height=Math.floor(t-n-c-r-2)+"px",e.style.height}(e);n(e,t)};window.addEventListener("resize",i().debounce(o,200),r),e._onResize={fn:o,options:r}},inserted:function(e){e._onResize&&(0,e._onResize.fn)(e)},componentUpdated:function(e){e._onResize&&(0,e._onResize.fn)(e)},unbind:function(e){if(e._onResize){var t=e._onResize,n=t.fn,r=t.options;window.removeEventListener("resize",n,r),delete e._onResize}}}},56904:(e,t,n)=>{var r=n(8081),i=n(23645)(r);i.push([e.id,".splitpanes.default-theme .splitpanes__pane[data-v-030dbc6e]{background-color:inherit}",""]),e.exports=i},51603:(e,t,n)=>{var r=n(56904);r.__esModule&&(r=r.default),"string"==typeof r&&(r=[[e.id,r,""]]),r.locals&&(e.exports=r.locals),(0,n(45346).Z)("48bc8808",r,!0,{})},80771:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>w}),n(85827),n(41539),n(68309),n(89554),n(54747),n(69070),n(47941),n(82526),n(57327),n(38880),n(49337),n(33321);var r=n(20144),i=n(72190),o=n(20629),s=n(99271),a=n(20376),c=n(92374);function u(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function l(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}const p={name:"Statistics",components:{Splitpanes:i.Splitpanes,Pane:i.Pane,ReportFilter:c.J},directives:{FillHeight:a.k},data:function(){var e=this,t=[{name:"Product Overview",icon:"mdi-briefcase-outline",to:{name:"product-overview"}},{name:"Checker Statistics",icon:"mdi-card-account-details",to:{name:"checker-statistics"}},{name:"Severity Statistics",icon:"mdi-speedometer",to:{name:"severity-statistics"}},{name:"Component Statistics",icon:"mdi-puzzle-outline",to:{name:"component-statistics"}}];return{namespace:"statistics",reportCount:0,tab:null,tabs:t,bus:new r.Z,refreshTabs:t.reduce((function(t,n){return t[e.$router.resolve(n.to).route.name]=!1,t}),{})}},computed:function(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?u(Object(n),!0).forEach((function(t){l(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):u(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}({},(0,o.rn)({runIds:function(e,t){return t["".concat(this.namespace,"/getRunIds")]},reportFilter:function(e,t){return t["".concat(this.namespace,"/getReportFilter")]}})),watch:{tab:function(){if(this.tab){var e=this.$router.resolve(this.tab);this.refreshTabs[e.route.name]&&this.refreshCurrentTab()}}},methods:{refresh:function(){var e=this;s.mv.getClient().getRunResultCount(this.runIds,this.reportFilter,null,(0,s.nC)((function(t){e.reportCount=t.toNumber()}))),this.tabs.forEach((function(t){var n=e.$router.resolve(t.to);e.refreshTabs[n.route.name]=!0})),this.refreshCurrentTab()},refreshCurrentTab:function(){this.bus.$emit("refresh");var e=this.$router.resolve(this.tab);this.refreshTabs[e.route.name]=!1}}};n(51603);var f=n(51900),h=n(43453),d=n.n(h),b=n(13047),m=n(92545),v=n(54160),g=(0,f.Z)(p,(function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("splitpanes",{staticClass:"default-theme"},[n("pane",{style:{"min-width":"300px"},attrs:{size:"20"}},[n("report-filter",{directives:[{name:"fill-height",rawName:"v-fill-height"}],attrs:{namespace:e.namespace,"show-remove-filtered-reports":!1,"report-count":e.reportCount,"show-diff-type":!1},on:{refresh:e.refresh}})],1),e._v(" "),n("pane",[n("div",{directives:[{name:"fill-height",rawName:"v-fill-height"}]},[n("v-tabs",{model:{value:e.tab,callback:function(t){e.tab=t},expression:"tab"}},e._l(e.tabs,(function(t){return n("v-tab",{key:t.name,attrs:{to:Object.assign({},t.to,{query:Object.assign({},e.$router.currentRoute.query)}),exact:""}},[n("v-icon",{staticClass:"mr-2"},[e._v("\n            "+e._s(t.icon)+"\n          ")]),e._v("\n          "+e._s(t.name)+"\n        ")],1)})),1),e._v(" "),n("keep-alive",[n("router-view",{attrs:{bus:e.bus,namespace:e.namespace}})],1)],1)])],1)}),[],!1,null,"030dbc6e",null);const w=g.exports;d()(g,{VIcon:b.Z,VTab:m.Z,VTabs:v.Z})}}]);