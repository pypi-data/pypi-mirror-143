(self.webpackChunkcodechecker=self.webpackChunkcodechecker||[]).push([[287],{52341:(e,r,t)=>{var n=t(8081),s=t(23645)(n);s.push([e.id,"#avatar[data-v-418b1461]{position:absolute;margin:0 auto;left:0;right:0;top:-70px;width:95px;height:95px;border-radius:50%;z-index:9;padding:15px;box-shadow:0px 2px 2px rgba(0,0,0,.1)}#login-btn[data-v-418b1461]{font-size:1.2em}",""]),e.exports=s},68404:(e,r,t)=>{var n=t(52341);n.__esModule&&(n=n.default),"string"==typeof n&&(n=[[e.id,n,""]]),n.locals&&(e.exports=n.locals),(0,t(45346).Z)("54e90fd4",n,!0,{})},52287:(e,r,t)=>{"use strict";t.r(r),t.d(r,{default:()=>j}),t(74916),t(15306),t(32564),t(69070),t(47941),t(82526),t(57327),t(41539),t(38880),t(89554),t(54747),t(49337),t(33321);var n=t(20629),s=t(3740);const o={name:"Alerts",props:{success:{type:Boolean,default:!1},error:{type:Boolean,default:!1},successMsg:{type:String,default:null},errorMsg:{type:String,default:null}}};var a=t(51900),l=t(43453),c=t.n(l),i=t(66897),u=(0,a.Z)(o,(function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("span",[t("v-alert",{attrs:{dismissible:"",color:"success",border:"left",elevation:"2","colored-border":"",icon:"mdi-check"},model:{value:e.success,callback:function(r){e.success=r},expression:"success"}},[e._v("\n    "+e._s(e.successMsg)+"\n  ")]),e._v(" "),t("v-alert",{attrs:{dismissible:"",color:"error",border:"left",elevation:"2","colored-border":"",icon:"mdi-alert-outline"},model:{value:e.error,callback:function(r){e.error=r},expression:"error"}},[e._v("\n    "+e._s(e.errorMsg)+"\n  ")])],1)}),[],!1,null,null,null);const d=u.exports;function p(e,r){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);r&&(n=n.filter((function(r){return Object.getOwnPropertyDescriptor(e,r).enumerable}))),t.push.apply(t,n)}return t}function f(e,r,t){return r in e?Object.defineProperty(e,r,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[r]=t,e}c()(u,{VAlert:i.Z});const v={name:"Login",components:{Alerts:d},data:function(){return{placeholder:null,username:null,password:null,success:!1,error:!1,errorMsg:null,valid:!1}},computed:function(e){for(var r=1;r<arguments.length;r++){var t=null!=arguments[r]?arguments[r]:{};r%2?p(Object(t),!0).forEach((function(r){f(e,r,t[r])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):p(Object(t)).forEach((function(r){Object.defineProperty(e,r,Object.getOwnPropertyDescriptor(t,r))}))}return e}({},(0,n.Se)(["isAuthenticated"])),watch:{username:function(){this.resetPlaceholder()},password:function(){this.resetPlaceholder()}},created:function(){this.isAuthenticated&&this.$router.replace({name:"products"})},mounted:function(){this.fixAutocomplete()},methods:{login:function(){var e=this;this.valid&&this.$store.dispatch(s.ym,{username:this.username,password:this.password}).then((function(){e.success=!0,e.error=!1;var r=e.$router.currentRoute.query.return_to;e.$router.replace(r||{name:"products"})})).catch((function(r){e.errorMsg="Failed to log in! ".concat(r.message),e.error=!0}))},fixAutocomplete:function(){var e=this,r=0,t=setInterval((function(){r+=1,(e.placeholder||20===r)&&clearInterval(t);var n=e.$el.querySelector('input[name="username"]:-webkit-autofill'),s=e.$el.querySelector('input[name="password"]:-webkit-autofill');(n||s)&&e.$nextTick((function(){e.placeholder="` `"}))}),100)},resetPlaceholder:function(){this.placeholder=null}}};t(68404);var m=t(35605),h=t(11880),b=t(74811),g=t(53544),y=t(55136),x=t(19846),k=t(58119),w=t(13047),_=t(90798),O=t(14462),C=(0,a.Z)(v,(function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("v-container",{staticClass:"fill-height",attrs:{fluid:""}},[t("v-row",{attrs:{align:"center",justify:"center"}},[t("v-col",{attrs:{cols:"12",sm:"8",md:"3"}},[t("v-card",{staticClass:"elevation-1 pa-8",attrs:{outlined:""}},[t("v-card-title",[t("v-container",{staticClass:"text-center pt-4"},[t("v-avatar",{attrs:{id:"avatar",color:"primary",size:120}},[t("v-icon",{attrs:{size:100,dark:""}},[e._v("\n                mdi-account\n              ")])],1),e._v(" "),t("div",{staticClass:"display-1 grey--text"},[e._v("\n              Login\n            ")])],1)],1),e._v(" "),t("v-card-text",{staticClass:"px-0 pb-0"},[t("alerts",{attrs:{success:e.success,"success-msg":"Successfully logged in!",error:e.error,"error-msg":e.errorMsg}}),e._v(" "),t("v-form",{model:{value:e.valid,callback:function(r){e.valid=r},expression:"valid"}},[t("v-text-field",{attrs:{autocomplete:"username",label:"Username",name:"username","append-icon":"mdi-account",type:"text",required:"",outlined:"",rules:[function(){return!!e.username||"This field is required"}],placeholder:e.placeholder},on:{keyup:function(r){return!r.type.indexOf("key")&&e._k(r.keyCode,"enter",13,r.key,"Enter")?null:e.login.apply(null,arguments)}},model:{value:e.username,callback:function(r){e.username=r},expression:"username"}}),e._v(" "),t("v-text-field",{attrs:{id:"password",autocomplete:"current-password",label:"Password",name:"password","append-icon":"mdi-lock",type:"password",required:"",outlined:"",rules:[function(){return!!e.password||"This field is required"}],placeholder:e.placeholder},on:{keyup:function(r){return!r.type.indexOf("key")&&e._k(r.keyCode,"enter",13,r.key,"Enter")?null:e.login.apply(null,arguments)}},model:{value:e.password,callback:function(r){e.password=r},expression:"password"}})],1)],1),e._v(" "),t("v-card-actions",{staticClass:"justify-center px-0"},[t("v-btn",{attrs:{id:"login-btn",block:"","x-large":"",color:"primary"},on:{click:e.login}},[e._v("\n            Login\n          ")])],1)],1)],1)],1)],1)}),[],!1,null,"418b1461",null);const j=C.exports;c()(C,{VAvatar:m.Z,VBtn:h.Z,VCard:b.Z,VCardActions:g.h7,VCardText:g.ZB,VCardTitle:g.EB,VCol:y.Z,VContainer:x.Z,VForm:k.Z,VIcon:w.Z,VRow:_.Z,VTextField:O.Z})}}]);