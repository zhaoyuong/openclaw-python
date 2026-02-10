(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const s of document.querySelectorAll('link[rel="modulepreload"]'))i(s);new MutationObserver(s=>{for(const a of s)if(a.type==="childList")for(const o of a.addedNodes)o.tagName==="LINK"&&o.rel==="modulepreload"&&i(o)}).observe(document,{childList:!0,subtree:!0});function n(s){const a={};return s.integrity&&(a.integrity=s.integrity),s.referrerPolicy&&(a.referrerPolicy=s.referrerPolicy),s.crossOrigin==="use-credentials"?a.credentials="include":s.crossOrigin==="anonymous"?a.credentials="omit":a.credentials="same-origin",a}function i(s){if(s.ep)return;s.ep=!0;const a=n(s);fetch(s.href,a)}})();const bn=globalThis,ls=bn.ShadowRoot&&(bn.ShadyCSS===void 0||bn.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,rs=Symbol(),$a=new WeakMap;let Vo=class{constructor(t,n,i){if(this._$cssResult$=!0,i!==rs)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=n}get styleSheet(){let t=this.o;const n=this.t;if(ls&&t===void 0){const i=n!==void 0&&n.length===1;i&&(t=$a.get(n)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&$a.set(n,t))}return t}toString(){return this.cssText}};const Nu=e=>new Vo(typeof e=="string"?e:e+"",void 0,rs),Ou=(e,...t)=>{const n=e.length===1?e[0]:t.reduce((i,s,a)=>i+(o=>{if(o._$cssResult$===!0)return o.cssText;if(typeof o=="number")return o;throw Error("Value passed to 'css' function must be a 'css' function result: "+o+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+e[a+1],e[0]);return new Vo(n,e,rs)},Du=(e,t)=>{if(ls)e.adoptedStyleSheets=t.map(n=>n instanceof CSSStyleSheet?n:n.styleSheet);else for(const n of t){const i=document.createElement("style"),s=bn.litNonce;s!==void 0&&i.setAttribute("nonce",s),i.textContent=n.cssText,e.appendChild(i)}},ka=ls?e=>e:e=>e instanceof CSSStyleSheet?(t=>{let n="";for(const i of t.cssRules)n+=i.cssText;return Nu(n)})(e):e;const{is:Bu,defineProperty:Uu,getOwnPropertyDescriptor:Ku,getOwnPropertyNames:zu,getOwnPropertySymbols:Hu,getPrototypeOf:ju}=Object,Pn=globalThis,Aa=Pn.trustedTypes,Gu=Aa?Aa.emptyScript:"",Wu=Pn.reactiveElementPolyfillSupport,Mt=(e,t)=>e,Sn={toAttribute(e,t){switch(t){case Boolean:e=e?Gu:null;break;case Object:case Array:e=e==null?e:JSON.stringify(e)}return e},fromAttribute(e,t){let n=e;switch(t){case Boolean:n=e!==null;break;case Number:n=e===null?null:Number(e);break;case Object:case Array:try{n=JSON.parse(e)}catch{n=null}}return n}},cs=(e,t)=>!Bu(e,t),Sa={attribute:!0,type:String,converter:Sn,reflect:!1,useDefault:!1,hasChanged:cs};Symbol.metadata??=Symbol("metadata"),Pn.litPropertyMetadata??=new WeakMap;let ut=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,n=Sa){if(n.state&&(n.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((n=Object.create(n)).wrapped=!0),this.elementProperties.set(t,n),!n.noAccessor){const i=Symbol(),s=this.getPropertyDescriptor(t,i,n);s!==void 0&&Uu(this.prototype,t,s)}}static getPropertyDescriptor(t,n,i){const{get:s,set:a}=Ku(this.prototype,t)??{get(){return this[n]},set(o){this[n]=o}};return{get:s,set(o){const l=s?.call(this);a?.call(this,o),this.requestUpdate(t,l,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Sa}static _$Ei(){if(this.hasOwnProperty(Mt("elementProperties")))return;const t=ju(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(Mt("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(Mt("properties"))){const n=this.properties,i=[...zu(n),...Hu(n)];for(const s of i)this.createProperty(s,n[s])}const t=this[Symbol.metadata];if(t!==null){const n=litPropertyMetadata.get(t);if(n!==void 0)for(const[i,s]of n)this.elementProperties.set(i,s)}this._$Eh=new Map;for(const[n,i]of this.elementProperties){const s=this._$Eu(n,i);s!==void 0&&this._$Eh.set(s,n)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){const n=[];if(Array.isArray(t)){const i=new Set(t.flat(1/0).reverse());for(const s of i)n.unshift(ka(s))}else t!==void 0&&n.push(ka(t));return n}static _$Eu(t,n){const i=n.attribute;return i===!1?void 0:typeof i=="string"?i:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),this.renderRoot!==void 0&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){const t=new Map,n=this.constructor.elementProperties;for(const i of n.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){const t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Du(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,n,i){this._$AK(t,i)}_$ET(t,n){const i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(s!==void 0&&i.reflect===!0){const a=(i.converter?.toAttribute!==void 0?i.converter:Sn).toAttribute(n,i.type);this._$Em=t,a==null?this.removeAttribute(s):this.setAttribute(s,a),this._$Em=null}}_$AK(t,n){const i=this.constructor,s=i._$Eh.get(t);if(s!==void 0&&this._$Em!==s){const a=i.getPropertyOptions(s),o=typeof a.converter=="function"?{fromAttribute:a.converter}:a.converter?.fromAttribute!==void 0?a.converter:Sn;this._$Em=s;const l=o.fromAttribute(n,a.type);this[s]=l??this._$Ej?.get(s)??l,this._$Em=null}}requestUpdate(t,n,i,s=!1,a){if(t!==void 0){const o=this.constructor;if(s===!1&&(a=this[t]),i??=o.getPropertyOptions(t),!((i.hasChanged??cs)(a,n)||i.useDefault&&i.reflect&&a===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,i))))return;this.C(t,n,i)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,n,{useDefault:i,reflect:s,wrapped:a},o){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??n??this[t]),a!==!0||o!==void 0)||(this._$AL.has(t)||(this.hasUpdated||i||(n=void 0),this._$AL.set(t,n)),s===!0&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(n){Promise.reject(n)}const t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(const[s,a]of this._$Ep)this[s]=a;this._$Ep=void 0}const i=this.constructor.elementProperties;if(i.size>0)for(const[s,a]of i){const{wrapped:o}=a,l=this[s];o!==!0||this._$AL.has(s)||l===void 0||this.C(s,void 0,a,l)}}let t=!1;const n=this._$AL;try{t=this.shouldUpdate(n),t?(this.willUpdate(n),this._$EO?.forEach(i=>i.hostUpdate?.()),this.update(n)):this._$EM()}catch(i){throw t=!1,this._$EM(),i}t&&this._$AE(n)}willUpdate(t){}_$AE(t){this._$EO?.forEach(n=>n.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(n=>this._$ET(n,this[n])),this._$EM()}updated(t){}firstUpdated(t){}};ut.elementStyles=[],ut.shadowRootOptions={mode:"open"},ut[Mt("elementProperties")]=new Map,ut[Mt("finalized")]=new Map,Wu?.({ReactiveElement:ut}),(Pn.reactiveElementVersions??=[]).push("2.1.2");const ds=globalThis,xa=e=>e,xn=ds.trustedTypes,_a=xn?xn.createPolicy("lit-html",{createHTML:e=>e}):void 0,Yo="$lit$",Pe=`lit$${Math.random().toFixed(9).slice(2)}$`,Qo="?"+Pe,qu=`<${Qo}>`,Qe=document,Bt=()=>Qe.createComment(""),Ut=e=>e===null||typeof e!="object"&&typeof e!="function",us=Array.isArray,Vu=e=>us(e)||typeof e?.[Symbol.iterator]=="function",ci=`[ 	
\f\r]`,wt=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Ca=/-->/g,Ea=/>/g,He=RegExp(`>|${ci}(?:([^\\s"'>=/]+)(${ci}*=${ci}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Ta=/'/g,La=/"/g,Jo=/^(?:script|style|textarea|title)$/i,Yu=e=>(t,...n)=>({_$litType$:e,strings:t,values:n}),r=Yu(1),Ne=Symbol.for("lit-noChange"),m=Symbol.for("lit-nothing"),Ia=new WeakMap,Ve=Qe.createTreeWalker(Qe,129);function Zo(e,t){if(!us(e)||!e.hasOwnProperty("raw"))throw Error("invalid template strings array");return _a!==void 0?_a.createHTML(t):t}const Qu=(e,t)=>{const n=e.length-1,i=[];let s,a=t===2?"<svg>":t===3?"<math>":"",o=wt;for(let l=0;l<n;l++){const d=e[l];let h,p,u=-1,y=0;for(;y<d.length&&(o.lastIndex=y,p=o.exec(d),p!==null);)y=o.lastIndex,o===wt?p[1]==="!--"?o=Ca:p[1]!==void 0?o=Ea:p[2]!==void 0?(Jo.test(p[2])&&(s=RegExp("</"+p[2],"g")),o=He):p[3]!==void 0&&(o=He):o===He?p[0]===">"?(o=s??wt,u=-1):p[1]===void 0?u=-2:(u=o.lastIndex-p[2].length,h=p[1],o=p[3]===void 0?He:p[3]==='"'?La:Ta):o===La||o===Ta?o=He:o===Ca||o===Ea?o=wt:(o=He,s=void 0);const v=o===He&&e[l+1].startsWith("/>")?" ":"";a+=o===wt?d+qu:u>=0?(i.push(h),d.slice(0,u)+Yo+d.slice(u)+Pe+v):d+Pe+(u===-2?l:v)}return[Zo(e,a+(e[n]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),i]};let Ii=class Xo{constructor({strings:t,_$litType$:n},i){let s;this.parts=[];let a=0,o=0;const l=t.length-1,d=this.parts,[h,p]=Qu(t,n);if(this.el=Xo.createElement(h,i),Ve.currentNode=this.el.content,n===2||n===3){const u=this.el.content.firstChild;u.replaceWith(...u.childNodes)}for(;(s=Ve.nextNode())!==null&&d.length<l;){if(s.nodeType===1){if(s.hasAttributes())for(const u of s.getAttributeNames())if(u.endsWith(Yo)){const y=p[o++],v=s.getAttribute(u).split(Pe),$=/([.?@])?(.*)/.exec(y);d.push({type:1,index:a,name:$[2],strings:v,ctor:$[1]==="."?Zu:$[1]==="?"?Xu:$[1]==="@"?ef:Nn}),s.removeAttribute(u)}else u.startsWith(Pe)&&(d.push({type:6,index:a}),s.removeAttribute(u));if(Jo.test(s.tagName)){const u=s.textContent.split(Pe),y=u.length-1;if(y>0){s.textContent=xn?xn.emptyScript:"";for(let v=0;v<y;v++)s.append(u[v],Bt()),Ve.nextNode(),d.push({type:2,index:++a});s.append(u[y],Bt())}}}else if(s.nodeType===8)if(s.data===Qo)d.push({type:2,index:a});else{let u=-1;for(;(u=s.data.indexOf(Pe,u+1))!==-1;)d.push({type:7,index:a}),u+=Pe.length-1}a++}}static createElement(t,n){const i=Qe.createElement("template");return i.innerHTML=t,i}};function ht(e,t,n=e,i){if(t===Ne)return t;let s=i!==void 0?n._$Co?.[i]:n._$Cl;const a=Ut(t)?void 0:t._$litDirective$;return s?.constructor!==a&&(s?._$AO?.(!1),a===void 0?s=void 0:(s=new a(e),s._$AT(e,n,i)),i!==void 0?(n._$Co??=[])[i]=s:n._$Cl=s),s!==void 0&&(t=ht(e,s._$AS(e,t.values),s,i)),t}class Ju{constructor(t,n){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=n}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){const{el:{content:n},parts:i}=this._$AD,s=(t?.creationScope??Qe).importNode(n,!0);Ve.currentNode=s;let a=Ve.nextNode(),o=0,l=0,d=i[0];for(;d!==void 0;){if(o===d.index){let h;d.type===2?h=new Fn(a,a.nextSibling,this,t):d.type===1?h=new d.ctor(a,d.name,d.strings,this,t):d.type===6&&(h=new tf(a,this,t)),this._$AV.push(h),d=i[++l]}o!==d?.index&&(a=Ve.nextNode(),o++)}return Ve.currentNode=Qe,s}p(t){let n=0;for(const i of this._$AV)i!==void 0&&(i.strings!==void 0?(i._$AI(t,i,n),n+=i.strings.length-2):i._$AI(t[n])),n++}}let Fn=class el{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,n,i,s){this.type=2,this._$AH=m,this._$AN=void 0,this._$AA=t,this._$AB=n,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode;const n=this._$AM;return n!==void 0&&t?.nodeType===11&&(t=n.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,n=this){t=ht(this,t,n),Ut(t)?t===m||t==null||t===""?(this._$AH!==m&&this._$AR(),this._$AH=m):t!==this._$AH&&t!==Ne&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):Vu(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==m&&Ut(this._$AH)?this._$AA.nextSibling.data=t:this.T(Qe.createTextNode(t)),this._$AH=t}$(t){const{values:n,_$litType$:i}=t,s=typeof i=="number"?this._$AC(t):(i.el===void 0&&(i.el=Ii.createElement(Zo(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(n);else{const a=new Ju(s,this),o=a.u(this.options);a.p(n),this.T(o),this._$AH=a}}_$AC(t){let n=Ia.get(t.strings);return n===void 0&&Ia.set(t.strings,n=new Ii(t)),n}k(t){us(this._$AH)||(this._$AH=[],this._$AR());const n=this._$AH;let i,s=0;for(const a of t)s===n.length?n.push(i=new el(this.O(Bt()),this.O(Bt()),this,this.options)):i=n[s],i._$AI(a),s++;s<n.length&&(this._$AR(i&&i._$AB.nextSibling,s),n.length=s)}_$AR(t=this._$AA.nextSibling,n){for(this._$AP?.(!1,!0,n);t!==this._$AB;){const i=xa(t).nextSibling;xa(t).remove(),t=i}}setConnected(t){this._$AM===void 0&&(this._$Cv=t,this._$AP?.(t))}};class Nn{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,n,i,s,a){this.type=1,this._$AH=m,this._$AN=void 0,this.element=t,this.name=n,this._$AM=s,this.options=a,i.length>2||i[0]!==""||i[1]!==""?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=m}_$AI(t,n=this,i,s){const a=this.strings;let o=!1;if(a===void 0)t=ht(this,t,n,0),o=!Ut(t)||t!==this._$AH&&t!==Ne,o&&(this._$AH=t);else{const l=t;let d,h;for(t=a[0],d=0;d<a.length-1;d++)h=ht(this,l[i+d],n,d),h===Ne&&(h=this._$AH[d]),o||=!Ut(h)||h!==this._$AH[d],h===m?t=m:t!==m&&(t+=(h??"")+a[d+1]),this._$AH[d]=h}o&&!s&&this.j(t)}j(t){t===m?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}}let Zu=class extends Nn{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===m?void 0:t}},Xu=class extends Nn{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==m)}},ef=class extends Nn{constructor(t,n,i,s,a){super(t,n,i,s,a),this.type=5}_$AI(t,n=this){if((t=ht(this,t,n,0)??m)===Ne)return;const i=this._$AH,s=t===m&&i!==m||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,a=t!==m&&(i===m||s);s&&this.element.removeEventListener(this.name,this,i),a&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){typeof this._$AH=="function"?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}},tf=class{constructor(t,n,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=n,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){ht(this,t)}};const nf={I:Fn},sf=ds.litHtmlPolyfillSupport;sf?.(Ii,Fn),(ds.litHtmlVersions??=[]).push("3.3.2");const af=(e,t,n)=>{const i=n?.renderBefore??t;let s=i._$litPart$;if(s===void 0){const a=n?.renderBefore??null;i._$litPart$=s=new Fn(t.insertBefore(Bt(),a),a,void 0,n??{})}return s._$AI(e),s};const fs=globalThis;let gt=class extends ut{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){const t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){const n=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=af(n,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return Ne}};gt._$litElement$=!0,gt.finalized=!0,fs.litElementHydrateSupport?.({LitElement:gt});const of=fs.litElementPolyfillSupport;of?.({LitElement:gt});(fs.litElementVersions??=[]).push("4.2.2");const tl=e=>(t,n)=>{n!==void 0?n.addInitializer(()=>{customElements.define(e,t)}):customElements.define(e,t)};const lf={attribute:!0,type:String,converter:Sn,reflect:!1,hasChanged:cs},rf=(e=lf,t,n)=>{const{kind:i,metadata:s}=n;let a=globalThis.litPropertyMetadata.get(s);if(a===void 0&&globalThis.litPropertyMetadata.set(s,a=new Map),i==="setter"&&((e=Object.create(e)).wrapped=!0),a.set(n.name,e),i==="accessor"){const{name:o}=n;return{set(l){const d=t.get.call(this);t.set.call(this,l),this.requestUpdate(o,d,e,!0,l)},init(l){return l!==void 0&&this.C(o,void 0,e,l),l}}}if(i==="setter"){const{name:o}=n;return function(l){const d=this[o];t.call(this,l),this.requestUpdate(o,d,e,!0,l)}}throw Error("Unsupported decorator location: "+i)};function yn(e){return(t,n)=>typeof n=="object"?rf(e,t,n):((i,s,a)=>{const o=s.hasOwnProperty(a);return s.constructor.createProperty(a,i),o?Object.getOwnPropertyDescriptor(s,a):void 0})(e,t,n)}function S(e){return yn({...e,state:!0,attribute:!1})}async function oe(e,t){if(!(!e.client||!e.connected)&&!e.channelsLoading){e.channelsLoading=!0,e.channelsError=null;try{const n=await e.client.request("channels.status",{probe:t,timeoutMs:8e3});e.channelsSnapshot=n,e.channelsLastSuccess=Date.now()}catch(n){e.channelsError=String(n)}finally{e.channelsLoading=!1}}}async function cf(e,t){if(!(!e.client||!e.connected||e.whatsappBusy)){e.whatsappBusy=!0;try{const n=await e.client.request("web.login.start",{force:t,timeoutMs:3e4});e.whatsappLoginMessage=n.message??null,e.whatsappLoginQrDataUrl=n.qrDataUrl??null,e.whatsappLoginConnected=null}catch(n){e.whatsappLoginMessage=String(n),e.whatsappLoginQrDataUrl=null,e.whatsappLoginConnected=null}finally{e.whatsappBusy=!1}}}async function df(e){if(!(!e.client||!e.connected||e.whatsappBusy)){e.whatsappBusy=!0;try{const t=await e.client.request("web.login.wait",{timeoutMs:12e4});e.whatsappLoginMessage=t.message??null,e.whatsappLoginConnected=t.connected??null,t.connected&&(e.whatsappLoginQrDataUrl=null)}catch(t){e.whatsappLoginMessage=String(t),e.whatsappLoginConnected=null}finally{e.whatsappBusy=!1}}}async function uf(e){if(!(!e.client||!e.connected||e.whatsappBusy)){e.whatsappBusy=!0;try{await e.client.request("channels.logout",{channel:"whatsapp"}),e.whatsappLoginMessage="Logged out.",e.whatsappLoginQrDataUrl=null,e.whatsappLoginConnected=null}catch(t){e.whatsappLoginMessage=String(t)}finally{e.whatsappBusy=!1}}}function Je(e){return typeof structuredClone=="function"?structuredClone(e):JSON.parse(JSON.stringify(e))}function pt(e){return`${JSON.stringify(e,null,2).trimEnd()}
`}function nl(e,t,n){if(t.length===0)return;let i=e;for(let a=0;a<t.length-1;a+=1){const o=t[a],l=t[a+1];if(typeof o=="number"){if(!Array.isArray(i))return;i[o]==null&&(i[o]=typeof l=="number"?[]:{}),i=i[o]}else{if(typeof i!="object"||i==null)return;const d=i;d[o]==null&&(d[o]=typeof l=="number"?[]:{}),i=d[o]}}const s=t[t.length-1];if(typeof s=="number"){Array.isArray(i)&&(i[s]=n);return}typeof i=="object"&&i!=null&&(i[s]=n)}function il(e,t){if(t.length===0)return;let n=e;for(let s=0;s<t.length-1;s+=1){const a=t[s];if(typeof a=="number"){if(!Array.isArray(n))return;n=n[a]}else{if(typeof n!="object"||n==null)return;n=n[a]}if(n==null)return}const i=t[t.length-1];if(typeof i=="number"){Array.isArray(n)&&n.splice(i,1);return}typeof n=="object"&&n!=null&&delete n[i]}async function me(e){if(!(!e.client||!e.connected)){e.configLoading=!0,e.lastError=null;try{const t=await e.client.request("config.get",{});gf(e,t)}catch(t){e.lastError=String(t)}finally{e.configLoading=!1}}}async function sl(e){if(!(!e.client||!e.connected)&&!e.configSchemaLoading){e.configSchemaLoading=!0;try{const t=await e.client.request("config.schema",{});ff(e,t)}catch(t){e.lastError=String(t)}finally{e.configSchemaLoading=!1}}}function ff(e,t){e.configSchema=t.schema??null,e.configUiHints=t.uiHints??{},e.configSchemaVersion=t.version??null}function gf(e,t){e.configSnapshot=t;const n=typeof t.raw=="string"?t.raw:t.config&&typeof t.config=="object"?pt(t.config):e.configRaw;!e.configFormDirty||e.configFormMode==="raw"?e.configRaw=n:e.configForm?e.configRaw=pt(e.configForm):e.configRaw=n,e.configValid=typeof t.valid=="boolean"?t.valid:null,e.configIssues=Array.isArray(t.issues)?t.issues:[],e.configFormDirty||(e.configForm=Je(t.config??{}),e.configFormOriginal=Je(t.config??{}),e.configRawOriginal=n)}async function wn(e){if(!(!e.client||!e.connected)){e.configSaving=!0,e.lastError=null;try{const t=e.configFormMode==="form"&&e.configForm?pt(e.configForm):e.configRaw,n=e.configSnapshot?.hash;if(!n){e.lastError="Config hash missing; reload and retry.";return}await e.client.request("config.set",{raw:t,baseHash:n}),e.configFormDirty=!1,await me(e)}catch(t){e.lastError=String(t)}finally{e.configSaving=!1}}}async function hf(e){if(!(!e.client||!e.connected)){e.configApplying=!0,e.lastError=null;try{const t=e.configFormMode==="form"&&e.configForm?pt(e.configForm):e.configRaw,n=e.configSnapshot?.hash;if(!n){e.lastError="Config hash missing; reload and retry.";return}await e.client.request("config.apply",{raw:t,baseHash:n,sessionKey:e.applySessionKey}),e.configFormDirty=!1,await me(e)}catch(t){e.lastError=String(t)}finally{e.configApplying=!1}}}async function pf(e){if(!(!e.client||!e.connected)){e.updateRunning=!0,e.lastError=null;try{await e.client.request("update.run",{sessionKey:e.applySessionKey})}catch(t){e.lastError=String(t)}finally{e.updateRunning=!1}}}function q(e,t,n){const i=Je(e.configForm??e.configSnapshot?.config??{});nl(i,t,n),e.configForm=i,e.configFormDirty=!0,e.configFormMode==="form"&&(e.configRaw=pt(i))}function ge(e,t){const n=Je(e.configForm??e.configSnapshot?.config??{});il(n,t),e.configForm=n,e.configFormDirty=!0,e.configFormMode==="form"&&(e.configRaw=pt(n))}function vf(e){const{values:t,original:n}=e;return t.name!==n.name||t.displayName!==n.displayName||t.about!==n.about||t.picture!==n.picture||t.banner!==n.banner||t.website!==n.website||t.nip05!==n.nip05||t.lud16!==n.lud16}function mf(e){const{state:t,callbacks:n,accountId:i}=e,s=vf(t),a=(l,d,h={})=>{const{type:p="text",placeholder:u,maxLength:y,help:v}=h,$=t.values[l]??"",g=t.fieldErrors[l],w=`nostr-profile-${l}`;return p==="textarea"?r`
        <div class="form-field" style="margin-bottom: 12px;">
          <label for="${w}" style="display: block; margin-bottom: 4px; font-weight: 500;">
            ${d}
          </label>
          <textarea
            id="${w}"
            .value=${$}
            placeholder=${u??""}
            maxlength=${y??2e3}
            rows="3"
            style="width: 100%; padding: 8px; border: 1px solid var(--border-color); border-radius: 4px; resize: vertical; font-family: inherit;"
            @input=${_=>{const C=_.target;n.onFieldChange(l,C.value)}}
            ?disabled=${t.saving}
          ></textarea>
          ${v?r`<div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">${v}</div>`:m}
          ${g?r`<div style="font-size: 12px; color: var(--danger-color); margin-top: 2px;">${g}</div>`:m}
        </div>
      `:r`
      <div class="form-field" style="margin-bottom: 12px;">
        <label for="${w}" style="display: block; margin-bottom: 4px; font-weight: 500;">
          ${d}
        </label>
        <input
          id="${w}"
          type=${p}
          .value=${$}
          placeholder=${u??""}
          maxlength=${y??256}
          style="width: 100%; padding: 8px; border: 1px solid var(--border-color); border-radius: 4px;"
          @input=${_=>{const C=_.target;n.onFieldChange(l,C.value)}}
          ?disabled=${t.saving}
        />
        ${v?r`<div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">${v}</div>`:m}
        ${g?r`<div style="font-size: 12px; color: var(--danger-color); margin-top: 2px;">${g}</div>`:m}
      </div>
    `},o=()=>{const l=t.values.picture;return l?r`
      <div style="margin-bottom: 12px;">
        <img
          src=${l}
          alt="Profile picture preview"
          style="max-width: 80px; max-height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid var(--border-color);"
          @error=${d=>{const h=d.target;h.style.display="none"}}
          @load=${d=>{const h=d.target;h.style.display="block"}}
        />
      </div>
    `:m};return r`
    <div class="nostr-profile-form" style="padding: 16px; background: var(--bg-secondary); border-radius: 8px; margin-top: 12px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <div style="font-weight: 600; font-size: 16px;">Edit Profile</div>
        <div style="font-size: 12px; color: var(--text-muted);">Account: ${i}</div>
      </div>

      ${t.error?r`<div class="callout danger" style="margin-bottom: 12px;">${t.error}</div>`:m}

      ${t.success?r`<div class="callout success" style="margin-bottom: 12px;">${t.success}</div>`:m}

      ${o()}

      ${a("name","Username",{placeholder:"satoshi",maxLength:256,help:"Short username (e.g., satoshi)"})}

      ${a("displayName","Display Name",{placeholder:"Satoshi Nakamoto",maxLength:256,help:"Your full display name"})}

      ${a("about","Bio",{type:"textarea",placeholder:"Tell people about yourself...",maxLength:2e3,help:"A brief bio or description"})}

      ${a("picture","Avatar URL",{type:"url",placeholder:"https://example.com/avatar.jpg",help:"HTTPS URL to your profile picture"})}

      ${t.showAdvanced?r`
            <div style="border-top: 1px solid var(--border-color); padding-top: 12px; margin-top: 12px;">
              <div style="font-weight: 500; margin-bottom: 12px; color: var(--text-muted);">Advanced</div>

              ${a("banner","Banner URL",{type:"url",placeholder:"https://example.com/banner.jpg",help:"HTTPS URL to a banner image"})}

              ${a("website","Website",{type:"url",placeholder:"https://example.com",help:"Your personal website"})}

              ${a("nip05","NIP-05 Identifier",{placeholder:"you@example.com",help:"Verifiable identifier (e.g., you@domain.com)"})}

              ${a("lud16","Lightning Address",{placeholder:"you@getalby.com",help:"Lightning address for tips (LUD-16)"})}
            </div>
          `:m}

      <div style="display: flex; gap: 8px; margin-top: 16px; flex-wrap: wrap;">
        <button
          class="btn primary"
          @click=${n.onSave}
          ?disabled=${t.saving||!s}
        >
          ${t.saving?"Saving...":"Save & Publish"}
        </button>

        <button
          class="btn"
          @click=${n.onImport}
          ?disabled=${t.importing||t.saving}
        >
          ${t.importing?"Importing...":"Import from Relays"}
        </button>

        <button
          class="btn"
          @click=${n.onToggleAdvanced}
        >
          ${t.showAdvanced?"Hide Advanced":"Show Advanced"}
        </button>

        <button
          class="btn"
          @click=${n.onCancel}
          ?disabled=${t.saving}
        >
          Cancel
        </button>
      </div>

      ${s?r`
              <div style="font-size: 12px; color: var(--warning-color); margin-top: 8px">
                You have unsaved changes
              </div>
            `:m}
    </div>
  `}function bf(e){const t={name:e?.name??"",displayName:e?.displayName??"",about:e?.about??"",picture:e?.picture??"",banner:e?.banner??"",website:e?.website??"",nip05:e?.nip05??"",lud16:e?.lud16??""};return{values:t,original:{...t},saving:!1,importing:!1,error:null,success:null,fieldErrors:{},showAdvanced:!!(e?.banner||e?.website||e?.nip05||e?.lud16)}}async function yf(e,t){await cf(e,t),await oe(e,!0)}async function wf(e){await df(e),await oe(e,!0)}async function $f(e){await uf(e),await oe(e,!0)}async function kf(e){await wn(e),await me(e),await oe(e,!0)}async function Af(e){await me(e),await oe(e,!0)}function Sf(e){if(!Array.isArray(e))return{};const t={};for(const n of e){if(typeof n!="string")continue;const[i,...s]=n.split(":");if(!i||s.length===0)continue;const a=i.trim(),o=s.join(":").trim();a&&o&&(t[a]=o)}return t}function al(e){return(e.channelsSnapshot?.channelAccounts?.nostr??[])[0]?.accountId??e.nostrProfileAccountId??"default"}function ol(e,t=""){return`/api/channels/nostr/${encodeURIComponent(e)}/profile${t}`}function xf(e,t,n){e.nostrProfileAccountId=t,e.nostrProfileFormState=bf(n??void 0)}function _f(e){e.nostrProfileFormState=null,e.nostrProfileAccountId=null}function Cf(e,t,n){const i=e.nostrProfileFormState;i&&(e.nostrProfileFormState={...i,values:{...i.values,[t]:n},fieldErrors:{...i.fieldErrors,[t]:""}})}function Ef(e){const t=e.nostrProfileFormState;t&&(e.nostrProfileFormState={...t,showAdvanced:!t.showAdvanced})}async function Tf(e){const t=e.nostrProfileFormState;if(!t||t.saving)return;const n=al(e);e.nostrProfileFormState={...t,saving:!0,error:null,success:null,fieldErrors:{}};try{const i=await fetch(ol(n),{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(t.values)}),s=await i.json().catch(()=>null);if(!i.ok||s?.ok===!1||!s){const a=s?.error??`Profile update failed (${i.status})`;e.nostrProfileFormState={...t,saving:!1,error:a,success:null,fieldErrors:Sf(s?.details)};return}if(!s.persisted){e.nostrProfileFormState={...t,saving:!1,error:"Profile publish failed on all relays.",success:null};return}e.nostrProfileFormState={...t,saving:!1,error:null,success:"Profile published to relays.",fieldErrors:{},original:{...t.values}},await oe(e,!0)}catch(i){e.nostrProfileFormState={...t,saving:!1,error:`Profile update failed: ${String(i)}`,success:null}}}async function Lf(e){const t=e.nostrProfileFormState;if(!t||t.importing)return;const n=al(e);e.nostrProfileFormState={...t,importing:!0,error:null,success:null};try{const i=await fetch(ol(n,"/import"),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({autoMerge:!0})}),s=await i.json().catch(()=>null);if(!i.ok||s?.ok===!1||!s){const d=s?.error??`Profile import failed (${i.status})`;e.nostrProfileFormState={...t,importing:!1,error:d,success:null};return}const a=s.merged??s.imported??null,o=a?{...t.values,...a}:t.values,l=!!(o.banner||o.website||o.nip05||o.lud16);e.nostrProfileFormState={...t,importing:!1,values:o,error:null,success:s.saved?"Profile imported from relays. Review and publish.":"Profile imported. Review and publish.",showAdvanced:l},s.saved&&await oe(e,!0)}catch(i){e.nostrProfileFormState={...t,importing:!1,error:`Profile import failed: ${String(i)}`,success:null}}}function ll(e){const t=(e??"").trim();if(!t)return null;const n=t.split(":").filter(Boolean);if(n.length<3||n[0]!=="agent")return null;const i=n[1]?.trim(),s=n.slice(2).join(":");return!i||!s?null:{agentId:i,rest:s}}const Ri=450;function Wt(e,t=!1){e.chatScrollFrame&&cancelAnimationFrame(e.chatScrollFrame),e.chatScrollTimeout!=null&&(clearTimeout(e.chatScrollTimeout),e.chatScrollTimeout=null);const n=()=>{const i=e.querySelector(".chat-thread");if(i){const s=getComputedStyle(i).overflowY;if(s==="auto"||s==="scroll"||i.scrollHeight-i.clientHeight>1)return i}return document.scrollingElement??document.documentElement};e.updateComplete.then(()=>{e.chatScrollFrame=requestAnimationFrame(()=>{e.chatScrollFrame=null;const i=n();if(!i)return;const s=i.scrollHeight-i.scrollTop-i.clientHeight,a=t&&!e.chatHasAutoScrolled;if(!(a||e.chatUserNearBottom||s<Ri)){e.chatNewMessagesBelow=!0;return}a&&(e.chatHasAutoScrolled=!0),i.scrollTop=i.scrollHeight,e.chatUserNearBottom=!0,e.chatNewMessagesBelow=!1;const l=a?150:120;e.chatScrollTimeout=window.setTimeout(()=>{e.chatScrollTimeout=null;const d=n();if(!d)return;const h=d.scrollHeight-d.scrollTop-d.clientHeight;(a||e.chatUserNearBottom||h<Ri)&&(d.scrollTop=d.scrollHeight,e.chatUserNearBottom=!0)},l)})})}function rl(e,t=!1){e.logsScrollFrame&&cancelAnimationFrame(e.logsScrollFrame),e.updateComplete.then(()=>{e.logsScrollFrame=requestAnimationFrame(()=>{e.logsScrollFrame=null;const n=e.querySelector(".log-stream");if(!n)return;const i=n.scrollHeight-n.scrollTop-n.clientHeight;(t||i<80)&&(n.scrollTop=n.scrollHeight)})})}function If(e,t){const n=t.currentTarget;if(!n)return;const i=n.scrollHeight-n.scrollTop-n.clientHeight;e.chatUserNearBottom=i<Ri,e.chatUserNearBottom&&(e.chatNewMessagesBelow=!1)}function Rf(e,t){const n=t.currentTarget;if(!n)return;const i=n.scrollHeight-n.scrollTop-n.clientHeight;e.logsAtBottom=i<80}function Ra(e){e.chatHasAutoScrolled=!1,e.chatUserNearBottom=!0,e.chatNewMessagesBelow=!1}function Mf(e,t){if(e.length===0)return;const n=new Blob([`${e.join(`
`)}
`],{type:"text/plain"}),i=URL.createObjectURL(n),s=document.createElement("a"),a=new Date().toISOString().slice(0,19).replace(/[:T]/g,"-");s.href=i,s.download=`openclaw-logs-${t}-${a}.log`,s.click(),URL.revokeObjectURL(i)}function Pf(e){if(typeof ResizeObserver>"u")return;const t=e.querySelector(".topbar");if(!t)return;const n=()=>{const{height:i}=t.getBoundingClientRect();e.style.setProperty("--topbar-height",`${i}px`)};n(),e.topbarObserver=new ResizeObserver(()=>n()),e.topbarObserver.observe(t)}async function On(e){if(!(!e.client||!e.connected)&&!e.debugLoading){e.debugLoading=!0;try{const[t,n,i,s]=await Promise.all([e.client.request("status",{}),e.client.request("health",{}),e.client.request("models.list",{}),e.client.request("last-heartbeat",{})]);e.debugStatus=t,e.debugHealth=n;const a=i;e.debugModels=Array.isArray(a?.models)?a?.models:[],e.debugHeartbeat=s}catch(t){e.debugCallError=String(t)}finally{e.debugLoading=!1}}}async function Ff(e){if(!(!e.client||!e.connected)){e.debugCallError=null,e.debugCallResult=null;try{const t=e.debugCallParams.trim()?JSON.parse(e.debugCallParams):{},n=await e.client.request(e.debugCallMethod.trim(),t);e.debugCallResult=JSON.stringify(n,null,2)}catch(t){e.debugCallError=String(t)}}}const Nf=2e3,Of=new Set(["trace","debug","info","warn","error","fatal"]);function Df(e){if(typeof e!="string")return null;const t=e.trim();if(!t.startsWith("{")||!t.endsWith("}"))return null;try{const n=JSON.parse(t);return!n||typeof n!="object"?null:n}catch{return null}}function Bf(e){if(typeof e!="string")return null;const t=e.toLowerCase();return Of.has(t)?t:null}function Uf(e){if(!e.trim())return{raw:e,message:e};try{const t=JSON.parse(e),n=t&&typeof t._meta=="object"&&t._meta!==null?t._meta:null,i=typeof t.time=="string"?t.time:typeof n?.date=="string"?n?.date:null,s=Bf(n?.logLevelName??n?.level),a=typeof t[0]=="string"?t[0]:typeof n?.name=="string"?n?.name:null,o=Df(a);let l=null;o&&(typeof o.subsystem=="string"?l=o.subsystem:typeof o.module=="string"&&(l=o.module)),!l&&a&&a.length<120&&(l=a);let d=null;return typeof t[1]=="string"?d=t[1]:!o&&typeof t[0]=="string"?d=t[0]:typeof t.message=="string"&&(d=t.message),{raw:e,time:i,level:s,subsystem:l,message:d??e,meta:n??void 0}}catch{return{raw:e,message:e}}}async function gs(e,t){if(!(!e.client||!e.connected)&&!(e.logsLoading&&!t?.quiet)){t?.quiet||(e.logsLoading=!0),e.logsError=null;try{const i=await e.client.request("logs.tail",{cursor:t?.reset?void 0:e.logsCursor??void 0,limit:e.logsLimit,maxBytes:e.logsMaxBytes}),a=(Array.isArray(i.lines)?i.lines.filter(l=>typeof l=="string"):[]).map(Uf),o=!!(t?.reset||i.reset||e.logsCursor==null);e.logsEntries=o?a:[...e.logsEntries,...a].slice(-Nf),typeof i.cursor=="number"&&(e.logsCursor=i.cursor),typeof i.file=="string"&&(e.logsFile=i.file),e.logsTruncated=!!i.truncated,e.logsLastFetchAt=Date.now()}catch(n){e.logsError=String(n)}finally{t?.quiet||(e.logsLoading=!1)}}}async function Dn(e,t){if(!(!e.client||!e.connected)&&!e.nodesLoading){e.nodesLoading=!0,t?.quiet||(e.lastError=null);try{const n=await e.client.request("node.list",{});e.nodes=Array.isArray(n.nodes)?n.nodes:[]}catch(n){t?.quiet||(e.lastError=String(n))}finally{e.nodesLoading=!1}}}function Kf(e){e.nodesPollInterval==null&&(e.nodesPollInterval=window.setInterval(()=>{Dn(e,{quiet:!0})},5e3))}function zf(e){e.nodesPollInterval!=null&&(clearInterval(e.nodesPollInterval),e.nodesPollInterval=null)}function hs(e){e.logsPollInterval==null&&(e.logsPollInterval=window.setInterval(()=>{e.tab==="logs"&&gs(e,{quiet:!0})},2e3))}function ps(e){e.logsPollInterval!=null&&(clearInterval(e.logsPollInterval),e.logsPollInterval=null)}function vs(e){e.debugPollInterval==null&&(e.debugPollInterval=window.setInterval(()=>{e.tab==="debug"&&On(e)},3e3))}function ms(e){e.debugPollInterval!=null&&(clearInterval(e.debugPollInterval),e.debugPollInterval=null)}async function cl(e,t){if(!(!e.client||!e.connected||e.agentIdentityLoading)&&!e.agentIdentityById[t]){e.agentIdentityLoading=!0,e.agentIdentityError=null;try{const n=await e.client.request("agent.identity.get",{agentId:t});n&&(e.agentIdentityById={...e.agentIdentityById,[t]:n})}catch(n){e.agentIdentityError=String(n)}finally{e.agentIdentityLoading=!1}}}async function dl(e,t){if(!e.client||!e.connected||e.agentIdentityLoading)return;const n=t.filter(i=>!e.agentIdentityById[i]);if(n.length!==0){e.agentIdentityLoading=!0,e.agentIdentityError=null;try{for(const i of n){const s=await e.client.request("agent.identity.get",{agentId:i});s&&(e.agentIdentityById={...e.agentIdentityById,[i]:s})}}catch(i){e.agentIdentityError=String(i)}finally{e.agentIdentityLoading=!1}}}async function $n(e,t){if(!(!e.client||!e.connected)&&!e.agentSkillsLoading){e.agentSkillsLoading=!0,e.agentSkillsError=null;try{const n=await e.client.request("skills.status",{agentId:t});n&&(e.agentSkillsReport=n,e.agentSkillsAgentId=t)}catch(n){e.agentSkillsError=String(n)}finally{e.agentSkillsLoading=!1}}}async function bs(e){if(!(!e.client||!e.connected)&&!e.agentsLoading){e.agentsLoading=!0,e.agentsError=null;try{const t=await e.client.request("agents.list",{});if(t){e.agentsList=t;const n=e.agentsSelectedId,i=t.agents.some(s=>s.id===n);(!n||!i)&&(e.agentsSelectedId=t.defaultId??t.agents[0]?.id??null)}}catch(t){e.agentsError=String(t)}finally{e.agentsLoading=!1}}}const Hf=/<\s*\/?\s*(?:think(?:ing)?|thought|antthinking|final)\b/i,rn=/<\s*\/?\s*final\b[^<>]*>/gi,Ma=/<\s*(\/?)\s*(?:think(?:ing)?|thought|antthinking)\b[^<>]*>/gi;function Pa(e){const t=[],n=/(^|\n)(```|~~~)[^\n]*\n[\s\S]*?(?:\n\2(?:\n|$)|$)/g;for(const s of e.matchAll(n)){const a=(s.index??0)+s[1].length;t.push({start:a,end:a+s[0].length-s[1].length})}const i=/`+[^`]+`+/g;for(const s of e.matchAll(i)){const a=s.index??0,o=a+s[0].length;t.some(d=>a>=d.start&&o<=d.end)||t.push({start:a,end:o})}return t.sort((s,a)=>s.start-a.start),t}function Fa(e,t){return t.some(n=>e>=n.start&&e<n.end)}function jf(e,t){return e.trimStart()}function Gf(e,t){if(!e||!Hf.test(e))return e;let n=e;if(rn.test(n)){rn.lastIndex=0;const l=[],d=Pa(n);for(const h of n.matchAll(rn)){const p=h.index??0;l.push({start:p,length:h[0].length,inCode:Fa(p,d)})}for(let h=l.length-1;h>=0;h--){const p=l[h];p.inCode||(n=n.slice(0,p.start)+n.slice(p.start+p.length))}}else rn.lastIndex=0;const i=Pa(n);Ma.lastIndex=0;let s="",a=0,o=!1;for(const l of n.matchAll(Ma)){const d=l.index??0,h=l[1]==="/";Fa(d,i)||(o?h&&(o=!1):(s+=n.slice(a,d),h||(o=!0)),a=d+l[0].length)}return s+=n.slice(a),jf(s)}function Kt(e){return!e&&e!==0?"n/a":new Date(e).toLocaleString()}function U(e){if(!e&&e!==0)return"n/a";const t=Date.now()-e,n=Math.abs(t),i=t<0?"from now":"ago",s=Math.round(n/1e3);if(s<60)return t<0?"just now":`${s}s ago`;const a=Math.round(s/60);if(a<60)return`${a}m ${i}`;const o=Math.round(a/60);return o<48?`${o}h ${i}`:`${Math.round(o/24)}d ${i}`}function ul(e){if(!e&&e!==0)return"n/a";if(e<1e3)return`${e}ms`;const t=Math.round(e/1e3);if(t<60)return`${t}s`;const n=Math.round(t/60);if(n<60)return`${n}m`;const i=Math.round(n/60);return i<48?`${i}h`:`${Math.round(i/24)}d`}function Mi(e){return!e||e.length===0?"none":e.filter(t=>!!(t&&t.trim())).join(", ")}function Pi(e,t=120){return e.length<=t?e:`${e.slice(0,Math.max(0,t-1))}…`}function fl(e,t){return e.length<=t?{text:e,truncated:!1,total:e.length}:{text:e.slice(0,Math.max(0,t)),truncated:!0,total:e.length}}function _n(e,t){const n=Number(e);return Number.isFinite(n)?n:t}function di(e){return Gf(e)}async function qt(e){if(!(!e.client||!e.connected))try{const t=await e.client.request("cron.status",{});e.cronStatus=t}catch(t){e.cronError=String(t)}}async function Bn(e){if(!(!e.client||!e.connected)&&!e.cronLoading){e.cronLoading=!0,e.cronError=null;try{const t=await e.client.request("cron.list",{includeDisabled:!0});e.cronJobs=Array.isArray(t.jobs)?t.jobs:[]}catch(t){e.cronError=String(t)}finally{e.cronLoading=!1}}}function Wf(e){if(e.scheduleKind==="at"){const n=Date.parse(e.scheduleAt);if(!Number.isFinite(n))throw new Error("Invalid run time.");return{kind:"at",at:new Date(n).toISOString()}}if(e.scheduleKind==="every"){const n=_n(e.everyAmount,0);if(n<=0)throw new Error("Invalid interval amount.");const i=e.everyUnit;return{kind:"every",everyMs:n*(i==="minutes"?6e4:i==="hours"?36e5:864e5)}}const t=e.cronExpr.trim();if(!t)throw new Error("Cron expression required.");return{kind:"cron",expr:t,tz:e.cronTz.trim()||void 0}}function qf(e){if(e.payloadKind==="systemEvent"){const s=e.payloadText.trim();if(!s)throw new Error("System event text required.");return{kind:"systemEvent",text:s}}const t=e.payloadText.trim();if(!t)throw new Error("Agent message required.");const n={kind:"agentTurn",message:t},i=_n(e.timeoutSeconds,0);return i>0&&(n.timeoutSeconds=i),n}async function Vf(e){if(!(!e.client||!e.connected||e.cronBusy)){e.cronBusy=!0,e.cronError=null;try{const t=Wf(e.cronForm),n=qf(e.cronForm),i=e.cronForm.sessionTarget==="isolated"&&e.cronForm.payloadKind==="agentTurn"&&e.cronForm.deliveryMode?{mode:e.cronForm.deliveryMode==="announce"?"announce":"none",channel:e.cronForm.deliveryChannel.trim()||"last",to:e.cronForm.deliveryTo.trim()||void 0}:void 0,s=e.cronForm.agentId.trim(),a={name:e.cronForm.name.trim(),description:e.cronForm.description.trim()||void 0,agentId:s||void 0,enabled:e.cronForm.enabled,schedule:t,sessionTarget:e.cronForm.sessionTarget,wakeMode:e.cronForm.wakeMode,payload:n,delivery:i};if(!a.name)throw new Error("Name required.");await e.client.request("cron.add",a),e.cronForm={...e.cronForm,name:"",description:"",payloadText:""},await Bn(e),await qt(e)}catch(t){e.cronError=String(t)}finally{e.cronBusy=!1}}}async function Yf(e,t,n){if(!(!e.client||!e.connected||e.cronBusy)){e.cronBusy=!0,e.cronError=null;try{await e.client.request("cron.update",{id:t.id,patch:{enabled:n}}),await Bn(e),await qt(e)}catch(i){e.cronError=String(i)}finally{e.cronBusy=!1}}}async function Qf(e,t){if(!(!e.client||!e.connected||e.cronBusy)){e.cronBusy=!0,e.cronError=null;try{await e.client.request("cron.run",{id:t.id,mode:"force"}),await gl(e,t.id)}catch(n){e.cronError=String(n)}finally{e.cronBusy=!1}}}async function Jf(e,t){if(!(!e.client||!e.connected||e.cronBusy)){e.cronBusy=!0,e.cronError=null;try{await e.client.request("cron.remove",{id:t.id}),e.cronRunsJobId===t.id&&(e.cronRunsJobId=null,e.cronRuns=[]),await Bn(e),await qt(e)}catch(n){e.cronError=String(n)}finally{e.cronBusy=!1}}}async function gl(e,t){if(!(!e.client||!e.connected))try{const n=await e.client.request("cron.runs",{id:t,limit:50});e.cronRunsJobId=t,e.cronRuns=Array.isArray(n.entries)?n.entries:[]}catch(n){e.cronError=String(n)}}const hl="openclaw.device.auth.v1";function ys(e){return e.trim()}function Zf(e){if(!Array.isArray(e))return[];const t=new Set;for(const n of e){const i=n.trim();i&&t.add(i)}return[...t].toSorted()}function ws(){try{const e=window.localStorage.getItem(hl);if(!e)return null;const t=JSON.parse(e);return!t||t.version!==1||!t.deviceId||typeof t.deviceId!="string"||!t.tokens||typeof t.tokens!="object"?null:t}catch{return null}}function pl(e){try{window.localStorage.setItem(hl,JSON.stringify(e))}catch{}}function Xf(e){const t=ws();if(!t||t.deviceId!==e.deviceId)return null;const n=ys(e.role),i=t.tokens[n];return!i||typeof i.token!="string"?null:i}function vl(e){const t=ys(e.role),n={version:1,deviceId:e.deviceId,tokens:{}},i=ws();i&&i.deviceId===e.deviceId&&(n.tokens={...i.tokens});const s={token:e.token,role:t,scopes:Zf(e.scopes),updatedAtMs:Date.now()};return n.tokens[t]=s,pl(n),s}function ml(e){const t=ws();if(!t||t.deviceId!==e.deviceId)return;const n=ys(e.role);if(!t.tokens[n])return;const i={...t,tokens:{...t.tokens}};delete i.tokens[n],pl(i)}const bl={p:0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffedn,n:0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3edn,h:8n,a:0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffecn,d:0x52036cee2b6ffe738cc740797779e89800700a4d4141d8ab75eb4dca135978a3n,Gx:0x216936d3cd6e53fec0a4e231fdd6dc5c692cc7609525a7b2c9562d608f25d51an,Gy:0x6666666666666666666666666666666666666666666666666666666666666658n},{p:ee,n:kn,Gx:Na,Gy:Oa,a:ui,d:fi,h:eg}=bl,Ze=32,$s=64,tg=(...e)=>{"captureStackTrace"in Error&&typeof Error.captureStackTrace=="function"&&Error.captureStackTrace(...e)},V=(e="")=>{const t=new Error(e);throw tg(t,V),t},ng=e=>typeof e=="bigint",ig=e=>typeof e=="string",sg=e=>e instanceof Uint8Array||ArrayBuffer.isView(e)&&e.constructor.name==="Uint8Array",De=(e,t,n="")=>{const i=sg(e),s=e?.length,a=t!==void 0;if(!i||a&&s!==t){const o=n&&`"${n}" `,l=a?` of length ${t}`:"",d=i?`length=${s}`:`type=${typeof e}`;V(o+"expected Uint8Array"+l+", got "+d)}return e},Un=e=>new Uint8Array(e),yl=e=>Uint8Array.from(e),wl=(e,t)=>e.toString(16).padStart(t,"0"),$l=e=>Array.from(De(e)).map(t=>wl(t,2)).join(""),Ee={_0:48,_9:57,A:65,F:70,a:97,f:102},Da=e=>{if(e>=Ee._0&&e<=Ee._9)return e-Ee._0;if(e>=Ee.A&&e<=Ee.F)return e-(Ee.A-10);if(e>=Ee.a&&e<=Ee.f)return e-(Ee.a-10)},kl=e=>{const t="hex invalid";if(!ig(e))return V(t);const n=e.length,i=n/2;if(n%2)return V(t);const s=Un(i);for(let a=0,o=0;a<i;a++,o+=2){const l=Da(e.charCodeAt(o)),d=Da(e.charCodeAt(o+1));if(l===void 0||d===void 0)return V(t);s[a]=l*16+d}return s},Al=()=>globalThis?.crypto,ag=()=>Al()?.subtle??V("crypto.subtle must be defined, consider polyfill"),zt=(...e)=>{const t=Un(e.reduce((i,s)=>i+De(s).length,0));let n=0;return e.forEach(i=>{t.set(i,n),n+=i.length}),t},og=(e=Ze)=>Al().getRandomValues(Un(e)),Cn=BigInt,We=(e,t,n,i="bad number: out of range")=>ng(e)&&t<=e&&e<n?e:V(i),R=(e,t=ee)=>{const n=e%t;return n>=0n?n:t+n},Sl=e=>R(e,kn),lg=(e,t)=>{(e===0n||t<=0n)&&V("no inverse n="+e+" mod="+t);let n=R(e,t),i=t,s=0n,a=1n;for(;n!==0n;){const o=i/n,l=i%n,d=s-a*o;i=n,n=l,s=a,a=d}return i===1n?R(s,t):V("no inverse")},rg=e=>{const t=El[e];return typeof t!="function"&&V("hashes."+e+" not set"),t},gi=e=>e instanceof re?e:V("Point expected"),Fi=2n**256n;class re{static BASE;static ZERO;X;Y;Z;T;constructor(t,n,i,s){const a=Fi;this.X=We(t,0n,a),this.Y=We(n,0n,a),this.Z=We(i,1n,a),this.T=We(s,0n,a),Object.freeze(this)}static CURVE(){return bl}static fromAffine(t){return new re(t.x,t.y,1n,R(t.x*t.y))}static fromBytes(t,n=!1){const i=fi,s=yl(De(t,Ze)),a=t[31];s[31]=a&-129;const o=_l(s);We(o,0n,n?Fi:ee);const d=R(o*o),h=R(d-1n),p=R(i*d+1n);let{isValid:u,value:y}=dg(h,p);u||V("bad point: y not sqrt");const v=(y&1n)===1n,$=(a&128)!==0;return!n&&y===0n&&$&&V("bad point: x==0, isLastByteOdd"),$!==v&&(y=R(-y)),new re(y,o,1n,R(y*o))}static fromHex(t,n){return re.fromBytes(kl(t),n)}get x(){return this.toAffine().x}get y(){return this.toAffine().y}assertValidity(){const t=ui,n=fi,i=this;if(i.is0())return V("bad point: ZERO");const{X:s,Y:a,Z:o,T:l}=i,d=R(s*s),h=R(a*a),p=R(o*o),u=R(p*p),y=R(d*t),v=R(p*R(y+h)),$=R(u+R(n*R(d*h)));if(v!==$)return V("bad point: equation left != right (1)");const g=R(s*a),w=R(o*l);return g!==w?V("bad point: equation left != right (2)"):this}equals(t){const{X:n,Y:i,Z:s}=this,{X:a,Y:o,Z:l}=gi(t),d=R(n*l),h=R(a*s),p=R(i*l),u=R(o*s);return d===h&&p===u}is0(){return this.equals(ft)}negate(){return new re(R(-this.X),this.Y,this.Z,R(-this.T))}double(){const{X:t,Y:n,Z:i}=this,s=ui,a=R(t*t),o=R(n*n),l=R(2n*R(i*i)),d=R(s*a),h=t+n,p=R(R(h*h)-a-o),u=d+o,y=u-l,v=d-o,$=R(p*y),g=R(u*v),w=R(p*v),_=R(y*u);return new re($,g,_,w)}add(t){const{X:n,Y:i,Z:s,T:a}=this,{X:o,Y:l,Z:d,T:h}=gi(t),p=ui,u=fi,y=R(n*o),v=R(i*l),$=R(a*u*h),g=R(s*d),w=R((n+i)*(o+l)-y-v),_=R(g-$),C=R(g+$),L=R(v-p*y),x=R(w*_),T=R(C*L),I=R(w*L),N=R(_*C);return new re(x,T,N,I)}subtract(t){return this.add(gi(t).negate())}multiply(t,n=!0){if(!n&&(t===0n||this.is0()))return ft;if(We(t,1n,kn),t===1n)return this;if(this.equals(Xe))return $g(t).p;let i=ft,s=Xe;for(let a=this;t>0n;a=a.double(),t>>=1n)t&1n?i=i.add(a):n&&(s=s.add(a));return i}multiplyUnsafe(t){return this.multiply(t,!1)}toAffine(){const{X:t,Y:n,Z:i}=this;if(this.equals(ft))return{x:0n,y:1n};const s=lg(i,ee);R(i*s)!==1n&&V("invalid inverse");const a=R(t*s),o=R(n*s);return{x:a,y:o}}toBytes(){const{x:t,y:n}=this.assertValidity().toAffine(),i=xl(n);return i[31]|=t&1n?128:0,i}toHex(){return $l(this.toBytes())}clearCofactor(){return this.multiply(Cn(eg),!1)}isSmallOrder(){return this.clearCofactor().is0()}isTorsionFree(){let t=this.multiply(kn/2n,!1).double();return kn%2n&&(t=t.add(this)),t.is0()}}const Xe=new re(Na,Oa,1n,R(Na*Oa)),ft=new re(0n,1n,1n,0n);re.BASE=Xe;re.ZERO=ft;const xl=e=>kl(wl(We(e,0n,Fi),$s)).reverse(),_l=e=>Cn("0x"+$l(yl(De(e)).reverse())),$e=(e,t)=>{let n=e;for(;t-- >0n;)n*=n,n%=ee;return n},cg=e=>{const n=e*e%ee*e%ee,i=$e(n,2n)*n%ee,s=$e(i,1n)*e%ee,a=$e(s,5n)*s%ee,o=$e(a,10n)*a%ee,l=$e(o,20n)*o%ee,d=$e(l,40n)*l%ee,h=$e(d,80n)*d%ee,p=$e(h,80n)*d%ee,u=$e(p,10n)*a%ee;return{pow_p_5_8:$e(u,2n)*e%ee,b2:n}},Ba=0x2b8324804fc1df0b2b4d00993dfbd7a72f431806ad2fe478c4ee1b274a0ea0b0n,dg=(e,t)=>{const n=R(t*t*t),i=R(n*n*t),s=cg(e*i).pow_p_5_8;let a=R(e*n*s);const o=R(t*a*a),l=a,d=R(a*Ba),h=o===e,p=o===R(-e),u=o===R(-e*Ba);return h&&(a=l),(p||u)&&(a=d),(R(a)&1n)===1n&&(a=R(-a)),{isValid:h||p,value:a}},Ni=e=>Sl(_l(e)),ks=(...e)=>El.sha512Async(zt(...e)),ug=(...e)=>rg("sha512")(zt(...e)),Cl=e=>{const t=e.slice(0,Ze);t[0]&=248,t[31]&=127,t[31]|=64;const n=e.slice(Ze,$s),i=Ni(t),s=Xe.multiply(i),a=s.toBytes();return{head:t,prefix:n,scalar:i,point:s,pointBytes:a}},As=e=>ks(De(e,Ze)).then(Cl),fg=e=>Cl(ug(De(e,Ze))),gg=e=>As(e).then(t=>t.pointBytes),hg=e=>ks(e.hashable).then(e.finish),pg=(e,t,n)=>{const{pointBytes:i,scalar:s}=e,a=Ni(t),o=Xe.multiply(a).toBytes();return{hashable:zt(o,i,n),finish:h=>{const p=Sl(a+Ni(h)*s);return De(zt(o,xl(p)),$s)}}},vg=async(e,t)=>{const n=De(e),i=await As(t),s=await ks(i.prefix,n);return hg(pg(i,s,n))},El={sha512Async:async e=>{const t=ag(),n=zt(e);return Un(await t.digest("SHA-512",n.buffer))},sha512:void 0},mg=(e=og(Ze))=>e,bg={getExtendedPublicKeyAsync:As,getExtendedPublicKey:fg,randomSecretKey:mg},En=8,yg=256,Tl=Math.ceil(yg/En)+1,Oi=2**(En-1),wg=()=>{const e=[];let t=Xe,n=t;for(let i=0;i<Tl;i++){n=t,e.push(n);for(let s=1;s<Oi;s++)n=n.add(t),e.push(n);t=n.double()}return e};let Ua;const Ka=(e,t)=>{const n=t.negate();return e?n:t},$g=e=>{const t=Ua||(Ua=wg());let n=ft,i=Xe;const s=2**En,a=s,o=Cn(s-1),l=Cn(En);for(let d=0;d<Tl;d++){let h=Number(e&o);e>>=l,h>Oi&&(h-=a,e+=1n);const p=d*Oi,u=p,y=p+Math.abs(h)-1,v=d%2!==0,$=h<0;h===0?i=i.add(Ka(v,t[u])):n=n.add(Ka($,t[y]))}return e!==0n&&V("invalid wnaf"),{p:n,f:i}},hi="openclaw-device-identity-v1";function Di(e){let t="";for(const n of e)t+=String.fromCharCode(n);return btoa(t).replaceAll("+","-").replaceAll("/","_").replace(/=+$/g,"")}function Ll(e){const t=e.replaceAll("-","+").replaceAll("_","/"),n=t+"=".repeat((4-t.length%4)%4),i=atob(n),s=new Uint8Array(i.length);for(let a=0;a<i.length;a+=1)s[a]=i.charCodeAt(a);return s}function kg(e){return Array.from(e).map(t=>t.toString(16).padStart(2,"0")).join("")}async function Il(e){const t=await crypto.subtle.digest("SHA-256",e.slice().buffer);return kg(new Uint8Array(t))}async function Ag(){const e=bg.randomSecretKey(),t=await gg(e);return{deviceId:await Il(t),publicKey:Di(t),privateKey:Di(e)}}async function Ss(){try{const n=localStorage.getItem(hi);if(n){const i=JSON.parse(n);if(i?.version===1&&typeof i.deviceId=="string"&&typeof i.publicKey=="string"&&typeof i.privateKey=="string"){const s=await Il(Ll(i.publicKey));if(s!==i.deviceId){const a={...i,deviceId:s};return localStorage.setItem(hi,JSON.stringify(a)),{deviceId:s,publicKey:i.publicKey,privateKey:i.privateKey}}return{deviceId:i.deviceId,publicKey:i.publicKey,privateKey:i.privateKey}}}}catch{}const e=await Ag(),t={version:1,deviceId:e.deviceId,publicKey:e.publicKey,privateKey:e.privateKey,createdAtMs:Date.now()};return localStorage.setItem(hi,JSON.stringify(t)),e}async function Sg(e,t){const n=Ll(e),i=new TextEncoder().encode(t),s=await vg(i,n);return Di(s)}async function Be(e,t){if(!(!e.client||!e.connected)&&!e.devicesLoading){e.devicesLoading=!0,t?.quiet||(e.devicesError=null);try{const n=await e.client.request("device.pair.list",{});e.devicesList={pending:Array.isArray(n?.pending)?n.pending:[],paired:Array.isArray(n?.paired)?n.paired:[]}}catch(n){t?.quiet||(e.devicesError=String(n))}finally{e.devicesLoading=!1}}}async function xg(e,t){if(!(!e.client||!e.connected))try{await e.client.request("device.pair.approve",{requestId:t}),await Be(e)}catch(n){e.devicesError=String(n)}}async function _g(e,t){if(!(!e.client||!e.connected||!window.confirm("Reject this device pairing request?")))try{await e.client.request("device.pair.reject",{requestId:t}),await Be(e)}catch(i){e.devicesError=String(i)}}async function Cg(e,t){if(!(!e.client||!e.connected))try{const n=await e.client.request("device.token.rotate",t);if(n?.token){const i=await Ss(),s=n.role??t.role;(n.deviceId===i.deviceId||t.deviceId===i.deviceId)&&vl({deviceId:i.deviceId,role:s,token:n.token,scopes:n.scopes??t.scopes??[]}),window.prompt("New device token (copy and store securely):",n.token)}await Be(e)}catch(n){e.devicesError=String(n)}}async function Eg(e,t){if(!(!e.client||!e.connected||!window.confirm(`Revoke token for ${t.deviceId} (${t.role})?`)))try{await e.client.request("device.token.revoke",t);const i=await Ss();t.deviceId===i.deviceId&&ml({deviceId:i.deviceId,role:t.role}),await Be(e)}catch(i){e.devicesError=String(i)}}function Tg(e){if(!e||e.kind==="gateway")return{method:"exec.approvals.get",params:{}};const t=e.nodeId.trim();return t?{method:"exec.approvals.node.get",params:{nodeId:t}}:null}function Lg(e,t){if(!e||e.kind==="gateway")return{method:"exec.approvals.set",params:t};const n=e.nodeId.trim();return n?{method:"exec.approvals.node.set",params:{...t,nodeId:n}}:null}async function xs(e,t){if(!(!e.client||!e.connected)&&!e.execApprovalsLoading){e.execApprovalsLoading=!0,e.lastError=null;try{const n=Tg(t);if(!n){e.lastError="Select a node before loading exec approvals.";return}const i=await e.client.request(n.method,n.params);Ig(e,i)}catch(n){e.lastError=String(n)}finally{e.execApprovalsLoading=!1}}}function Ig(e,t){e.execApprovalsSnapshot=t,e.execApprovalsDirty||(e.execApprovalsForm=Je(t.file??{}))}async function Rg(e,t){if(!(!e.client||!e.connected)){e.execApprovalsSaving=!0,e.lastError=null;try{const n=e.execApprovalsSnapshot?.hash;if(!n){e.lastError="Exec approvals hash missing; reload and retry.";return}const i=e.execApprovalsForm??e.execApprovalsSnapshot?.file??{},s=Lg(t,{file:i,baseHash:n});if(!s){e.lastError="Select a node before saving exec approvals.";return}await e.client.request(s.method,s.params),e.execApprovalsDirty=!1,await xs(e,t)}catch(n){e.lastError=String(n)}finally{e.execApprovalsSaving=!1}}}function Mg(e,t,n){const i=Je(e.execApprovalsForm??e.execApprovalsSnapshot?.file??{});nl(i,t,n),e.execApprovalsForm=i,e.execApprovalsDirty=!0}function Pg(e,t){const n=Je(e.execApprovalsForm??e.execApprovalsSnapshot?.file??{});il(n,t),e.execApprovalsForm=n,e.execApprovalsDirty=!0}async function _s(e){if(!(!e.client||!e.connected)&&!e.presenceLoading){e.presenceLoading=!0,e.presenceError=null,e.presenceStatus=null;try{const t=await e.client.request("system-presence",{});Array.isArray(t)?(e.presenceEntries=t,e.presenceStatus=t.length===0?"No instances yet.":null):(e.presenceEntries=[],e.presenceStatus="No presence payload.")}catch(t){e.presenceError=String(t)}finally{e.presenceLoading=!1}}}async function nt(e,t){if(!(!e.client||!e.connected)&&!e.sessionsLoading){e.sessionsLoading=!0,e.sessionsError=null;try{const n=t?.includeGlobal??e.sessionsIncludeGlobal,i=t?.includeUnknown??e.sessionsIncludeUnknown,s=t?.activeMinutes??_n(e.sessionsFilterActive,0),a=t?.limit??_n(e.sessionsFilterLimit,0),o={includeGlobal:n,includeUnknown:i};s>0&&(o.activeMinutes=s),a>0&&(o.limit=a);const l=await e.client.request("sessions.list",o);l&&(e.sessionsResult=l)}catch(n){e.sessionsError=String(n)}finally{e.sessionsLoading=!1}}}async function Fg(e,t,n){if(!e.client||!e.connected)return;const i={key:t};"label"in n&&(i.label=n.label),"thinkingLevel"in n&&(i.thinkingLevel=n.thinkingLevel),"verboseLevel"in n&&(i.verboseLevel=n.verboseLevel),"reasoningLevel"in n&&(i.reasoningLevel=n.reasoningLevel);try{await e.client.request("sessions.patch",i),await nt(e)}catch(s){e.sessionsError=String(s)}}async function Ng(e,t){if(!(!e.client||!e.connected||e.sessionsLoading||!window.confirm(`Delete session "${t}"?

Deletes the session entry and archives its transcript.`))){e.sessionsLoading=!0,e.sessionsError=null;try{await e.client.request("sessions.delete",{key:t,deleteTranscript:!0}),await nt(e)}catch(i){e.sessionsError=String(i)}finally{e.sessionsLoading=!1}}}function vt(e,t,n){if(!t.trim())return;const i={...e.skillMessages};n?i[t]=n:delete i[t],e.skillMessages=i}function Kn(e){return e instanceof Error?e.message:String(e)}async function Vt(e,t){if(t?.clearMessages&&Object.keys(e.skillMessages).length>0&&(e.skillMessages={}),!(!e.client||!e.connected)&&!e.skillsLoading){e.skillsLoading=!0,e.skillsError=null;try{const n=await e.client.request("skills.status",{});n&&(e.skillsReport=n)}catch(n){e.skillsError=Kn(n)}finally{e.skillsLoading=!1}}}function Og(e,t,n){e.skillEdits={...e.skillEdits,[t]:n}}async function Dg(e,t,n){if(!(!e.client||!e.connected)){e.skillsBusyKey=t,e.skillsError=null;try{await e.client.request("skills.update",{skillKey:t,enabled:n}),await Vt(e),vt(e,t,{kind:"success",message:n?"Skill enabled":"Skill disabled"})}catch(i){const s=Kn(i);e.skillsError=s,vt(e,t,{kind:"error",message:s})}finally{e.skillsBusyKey=null}}}async function Bg(e,t){if(!(!e.client||!e.connected)){e.skillsBusyKey=t,e.skillsError=null;try{const n=e.skillEdits[t]??"";await e.client.request("skills.update",{skillKey:t,apiKey:n}),await Vt(e),vt(e,t,{kind:"success",message:"API key saved"})}catch(n){const i=Kn(n);e.skillsError=i,vt(e,t,{kind:"error",message:i})}finally{e.skillsBusyKey=null}}}async function Ug(e,t,n,i){if(!(!e.client||!e.connected)){e.skillsBusyKey=t,e.skillsError=null;try{const s=await e.client.request("skills.install",{name:n,installId:i,timeoutMs:12e4});await Vt(e),vt(e,t,{kind:"success",message:s?.message??"Installed"})}catch(s){const a=Kn(s);e.skillsError=a,vt(e,t,{kind:"error",message:a})}finally{e.skillsBusyKey=null}}}const Kg=[{label:"Chat",tabs:["chat"]},{label:"Control",tabs:["overview","channels","instances","sessions","cron"]},{label:"Agent",tabs:["agents","skills","nodes"]},{label:"Settings",tabs:["config","debug","logs"]}],Rl={agents:"/agents",overview:"/overview",channels:"/channels",instances:"/instances",sessions:"/sessions",cron:"/cron",skills:"/skills",nodes:"/nodes",chat:"/chat",config:"/config",debug:"/debug",logs:"/logs"},Ml=new Map(Object.entries(Rl).map(([e,t])=>[t,e]));function Yt(e){if(!e)return"";let t=e.trim();return t.startsWith("/")||(t=`/${t}`),t==="/"?"":(t.endsWith("/")&&(t=t.slice(0,-1)),t)}function Ht(e){if(!e)return"/";let t=e.trim();return t.startsWith("/")||(t=`/${t}`),t.length>1&&t.endsWith("/")&&(t=t.slice(0,-1)),t}function Cs(e,t=""){const n=Yt(t),i=Rl[e];return n?`${n}${i}`:i}function Pl(e,t=""){const n=Yt(t);let i=e||"/";n&&(i===n?i="/":i.startsWith(`${n}/`)&&(i=i.slice(n.length)));let s=Ht(i).toLowerCase();return s.endsWith("/index.html")&&(s="/"),s==="/"?"chat":Ml.get(s)??null}function zg(e){let t=Ht(e);if(t.endsWith("/index.html")&&(t=Ht(t.slice(0,-11))),t==="/")return"";const n=t.split("/").filter(Boolean);if(n.length===0)return"";for(let i=0;i<n.length;i++){const s=`/${n.slice(i).join("/")}`.toLowerCase();if(Ml.has(s)){const a=n.slice(0,i);return a.length?`/${a.join("/")}`:""}}return`/${n.join("/")}`}function Hg(e){switch(e){case"agents":return"folder";case"chat":return"messageSquare";case"overview":return"barChart";case"channels":return"link";case"instances":return"radio";case"sessions":return"fileText";case"cron":return"loader";case"skills":return"zap";case"nodes":return"monitor";case"config":return"settings";case"debug":return"bug";case"logs":return"scrollText";default:return"folder"}}function Bi(e){switch(e){case"agents":return"Agents";case"overview":return"Overview";case"channels":return"Channels";case"instances":return"Instances";case"sessions":return"Sessions";case"cron":return"Cron Jobs";case"skills":return"Skills";case"nodes":return"Nodes";case"chat":return"Chat";case"config":return"Config";case"debug":return"Debug";case"logs":return"Logs";default:return"Control"}}function jg(e){switch(e){case"agents":return"Manage agent workspaces, tools, and identities.";case"overview":return"Gateway status, entry points, and a fast health read.";case"channels":return"Manage channels and settings.";case"instances":return"Presence beacons from connected clients and nodes.";case"sessions":return"Inspect active sessions and adjust per-session defaults.";case"cron":return"Schedule wakeups and recurring agent runs.";case"skills":return"Manage skill availability and API key injection.";case"nodes":return"Paired devices, capabilities, and command exposure.";case"chat":return"Direct gateway chat session for quick interventions.";case"config":return"Edit ~/.openclaw/openclaw.json safely.";case"debug":return"Gateway snapshots, events, and manual RPC calls.";case"logs":return"Live tail of the gateway file logs.";default:return""}}const Fl="openclaw.control.settings.v1";function Gg(){const t={gatewayUrl:`${location.protocol==="https:"?"wss":"ws"}://${location.host}`,token:"",sessionKey:"main",lastActiveSessionKey:"main",theme:"system",chatFocusMode:!1,chatShowThinking:!0,splitRatio:.6,navCollapsed:!1,navGroupsCollapsed:{}};try{const n=localStorage.getItem(Fl);if(!n)return t;const i=JSON.parse(n);return{gatewayUrl:typeof i.gatewayUrl=="string"&&i.gatewayUrl.trim()?i.gatewayUrl.trim():t.gatewayUrl,token:typeof i.token=="string"?i.token:t.token,sessionKey:typeof i.sessionKey=="string"&&i.sessionKey.trim()?i.sessionKey.trim():t.sessionKey,lastActiveSessionKey:typeof i.lastActiveSessionKey=="string"&&i.lastActiveSessionKey.trim()?i.lastActiveSessionKey.trim():typeof i.sessionKey=="string"&&i.sessionKey.trim()||t.lastActiveSessionKey,theme:i.theme==="light"||i.theme==="dark"||i.theme==="system"?i.theme:t.theme,chatFocusMode:typeof i.chatFocusMode=="boolean"?i.chatFocusMode:t.chatFocusMode,chatShowThinking:typeof i.chatShowThinking=="boolean"?i.chatShowThinking:t.chatShowThinking,splitRatio:typeof i.splitRatio=="number"&&i.splitRatio>=.4&&i.splitRatio<=.7?i.splitRatio:t.splitRatio,navCollapsed:typeof i.navCollapsed=="boolean"?i.navCollapsed:t.navCollapsed,navGroupsCollapsed:typeof i.navGroupsCollapsed=="object"&&i.navGroupsCollapsed!==null?i.navGroupsCollapsed:t.navGroupsCollapsed}}catch{return t}}function Wg(e){localStorage.setItem(Fl,JSON.stringify(e))}const cn=e=>Number.isNaN(e)?.5:e<=0?0:e>=1?1:e,qg=()=>typeof window>"u"||typeof window.matchMedia!="function"?!1:window.matchMedia("(prefers-reduced-motion: reduce)").matches??!1,dn=e=>{e.classList.remove("theme-transition"),e.style.removeProperty("--theme-switch-x"),e.style.removeProperty("--theme-switch-y")},Vg=({nextTheme:e,applyTheme:t,context:n,currentTheme:i})=>{if(i===e)return;const s=globalThis.document??null;if(!s){t();return}const a=s.documentElement,o=s,l=qg();if(!!o.startViewTransition&&!l){let h=.5,p=.5;if(n?.pointerClientX!==void 0&&n?.pointerClientY!==void 0&&typeof window<"u")h=cn(n.pointerClientX/window.innerWidth),p=cn(n.pointerClientY/window.innerHeight);else if(n?.element){const u=n.element.getBoundingClientRect();u.width>0&&u.height>0&&typeof window<"u"&&(h=cn((u.left+u.width/2)/window.innerWidth),p=cn((u.top+u.height/2)/window.innerHeight))}a.style.setProperty("--theme-switch-x",`${h*100}%`),a.style.setProperty("--theme-switch-y",`${p*100}%`),a.classList.add("theme-transition");try{const u=o.startViewTransition?.(()=>{t()});u?.finished?u.finished.finally(()=>dn(a)):dn(a)}catch{dn(a),t()}return}t(),dn(a)};function Yg(){return typeof window>"u"||typeof window.matchMedia!="function"||window.matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}function Es(e){return e==="system"?Yg():e}function Qg(){try{return window.top===window.self}catch{return!1}}function Jg(e){const t=e.trim();if(!t)return null;try{const n=new URL(t);return n.protocol!=="ws:"&&n.protocol!=="wss:"?null:t}catch{return null}}function Oe(e,t){const n={...t,lastActiveSessionKey:t.lastActiveSessionKey?.trim()||t.sessionKey.trim()||"main"};e.settings=n,Wg(n),t.theme!==e.theme&&(e.theme=t.theme,zn(e,Es(t.theme))),e.applySessionKey=e.settings.lastActiveSessionKey}function Nl(e,t){const n=t.trim();n&&e.settings.lastActiveSessionKey!==n&&Oe(e,{...e.settings,lastActiveSessionKey:n})}function Zg(e){if(!window.location.search)return;const t=new URLSearchParams(window.location.search),n=t.get("token"),i=t.get("password"),s=t.get("session"),a=t.get("gatewayUrl");let o=!1;if(n!=null){const d=n.trim();d&&d!==e.settings.token&&Oe(e,{...e.settings,token:d}),t.delete("token"),o=!0}if(i!=null){const d=i.trim();d&&(e.password=d),t.delete("password"),o=!0}if(s!=null){const d=s.trim();d&&(e.sessionKey=d,Oe(e,{...e.settings,sessionKey:d,lastActiveSessionKey:d}))}if(a!=null){const d=Jg(a);d&&d!==e.settings.gatewayUrl&&Qg()&&(e.pendingGatewayUrl=d),t.delete("gatewayUrl"),o=!0}if(!o)return;const l=new URL(window.location.href);l.search=t.toString(),window.history.replaceState({},"",l.toString())}function Xg(e,t){e.tab!==t&&(e.tab=t),t==="chat"&&(e.chatHasAutoScrolled=!1),t==="logs"?hs(e):ps(e),t==="debug"?vs(e):ms(e),Ts(e),Dl(e,t,!1)}function eh(e,t,n){Vg({nextTheme:t,applyTheme:()=>{e.theme=t,Oe(e,{...e.settings,theme:t}),zn(e,Es(t))},context:n,currentTheme:e.theme})}async function Ts(e){if(e.tab==="overview"&&await Bl(e),e.tab==="channels"&&await rh(e),e.tab==="instances"&&await _s(e),e.tab==="sessions"&&await nt(e),e.tab==="cron"&&await Tn(e),e.tab==="skills"&&await Vt(e),e.tab==="agents"){const t=e;await bs(t),await me(t);const n=t.agentsList?.agents?.map(s=>s.id)??[];n.length>0&&dl(t,n);const i=t.agentsSelectedId??t.agentsList?.defaultId??t.agentsList?.agents?.[0]?.id;i&&(cl(t,i),t.agentsPanel==="skills"&&$n(t,i),t.agentsPanel==="channels"&&oe(t,!1),t.agentsPanel==="cron"&&Tn(e))}e.tab==="nodes"&&(await Dn(e),await Be(e),await me(e),await xs(e)),e.tab==="chat"&&(await Wl(e),Wt(e,!e.chatHasAutoScrolled)),e.tab==="config"&&(await sl(e),await me(e)),e.tab==="debug"&&(await On(e),e.eventLog=e.eventLogBuffer),e.tab==="logs"&&(e.logsAtBottom=!0,await gs(e,{reset:!0}),rl(e,!0))}function th(){if(typeof window>"u")return"";const e=window.__OPENCLAW_CONTROL_UI_BASE_PATH__;return typeof e=="string"&&e.trim()?Yt(e):zg(window.location.pathname)}function nh(e){e.theme=e.settings.theme??"system",zn(e,Es(e.theme))}function zn(e,t){if(e.themeResolved=t,typeof document>"u")return;const n=document.documentElement;n.dataset.theme=t,n.style.colorScheme=t}function ih(e){if(typeof window>"u"||typeof window.matchMedia!="function")return;if(e.themeMedia=window.matchMedia("(prefers-color-scheme: dark)"),e.themeMediaHandler=n=>{e.theme==="system"&&zn(e,n.matches?"dark":"light")},typeof e.themeMedia.addEventListener=="function"){e.themeMedia.addEventListener("change",e.themeMediaHandler);return}e.themeMedia.addListener(e.themeMediaHandler)}function sh(e){if(!e.themeMedia||!e.themeMediaHandler)return;if(typeof e.themeMedia.removeEventListener=="function"){e.themeMedia.removeEventListener("change",e.themeMediaHandler);return}e.themeMedia.removeListener(e.themeMediaHandler),e.themeMedia=null,e.themeMediaHandler=null}function ah(e,t){if(typeof window>"u")return;const n=Pl(window.location.pathname,e.basePath)??"chat";Ol(e,n),Dl(e,n,t)}function oh(e){if(typeof window>"u")return;const t=Pl(window.location.pathname,e.basePath);if(!t)return;const i=new URL(window.location.href).searchParams.get("session")?.trim();i&&(e.sessionKey=i,Oe(e,{...e.settings,sessionKey:i,lastActiveSessionKey:i})),Ol(e,t)}function Ol(e,t){e.tab!==t&&(e.tab=t),t==="chat"&&(e.chatHasAutoScrolled=!1),t==="logs"?hs(e):ps(e),t==="debug"?vs(e):ms(e),e.connected&&Ts(e)}function Dl(e,t,n){if(typeof window>"u")return;const i=Ht(Cs(t,e.basePath)),s=Ht(window.location.pathname),a=new URL(window.location.href);t==="chat"&&e.sessionKey?a.searchParams.set("session",e.sessionKey):a.searchParams.delete("session"),s!==i&&(a.pathname=i),n?window.history.replaceState({},"",a.toString()):window.history.pushState({},"",a.toString())}function lh(e,t){if(typeof window>"u")return;const n=new URL(window.location.href);n.searchParams.set("session",e),window.history.replaceState({},"",n.toString())}async function Bl(e){await Promise.all([oe(e,!1),_s(e),nt(e),qt(e),On(e)])}async function rh(e){await Promise.all([oe(e,!0),sl(e),me(e)])}async function Tn(e){await Promise.all([oe(e,!1),qt(e),Bn(e)])}const za=50,ch=80,dh=12e4;function uh(e){if(!e||typeof e!="object")return null;const t=e;if(typeof t.text=="string")return t.text;const n=t.content;if(!Array.isArray(n))return null;const i=n.map(s=>{if(!s||typeof s!="object")return null;const a=s;return a.type==="text"&&typeof a.text=="string"?a.text:null}).filter(s=>!!s);return i.length===0?null:i.join(`
`)}function Ha(e){if(e==null)return null;if(typeof e=="number"||typeof e=="boolean")return String(e);const t=uh(e);let n;if(typeof e=="string")n=e;else if(t)n=t;else try{n=JSON.stringify(e,null,2)}catch{n=String(e)}const i=fl(n,dh);return i.truncated?`${i.text}

… truncated (${i.total} chars, showing first ${i.text.length}).`:i.text}function fh(e){const t=[];return t.push({type:"toolcall",name:e.name,arguments:e.args??{}}),e.output&&t.push({type:"toolresult",name:e.name,text:e.output}),{role:"assistant",toolCallId:e.toolCallId,runId:e.runId,content:t,timestamp:e.startedAt}}function gh(e){if(e.toolStreamOrder.length<=za)return;const t=e.toolStreamOrder.length-za,n=e.toolStreamOrder.splice(0,t);for(const i of n)e.toolStreamById.delete(i)}function hh(e){e.chatToolMessages=e.toolStreamOrder.map(t=>e.toolStreamById.get(t)?.message).filter(t=>!!t)}function Ui(e){e.toolStreamSyncTimer!=null&&(clearTimeout(e.toolStreamSyncTimer),e.toolStreamSyncTimer=null),hh(e)}function ph(e,t=!1){if(t){Ui(e);return}e.toolStreamSyncTimer==null&&(e.toolStreamSyncTimer=window.setTimeout(()=>Ui(e),ch))}function Hn(e){e.toolStreamById.clear(),e.toolStreamOrder=[],e.chatToolMessages=[],Ui(e)}const vh=5e3;function mh(e,t){const n=t.data??{},i=typeof n.phase=="string"?n.phase:"";e.compactionClearTimer!=null&&(window.clearTimeout(e.compactionClearTimer),e.compactionClearTimer=null),i==="start"?e.compactionStatus={active:!0,startedAt:Date.now(),completedAt:null}:i==="end"&&(e.compactionStatus={active:!1,startedAt:e.compactionStatus?.startedAt??null,completedAt:Date.now()},e.compactionClearTimer=window.setTimeout(()=>{e.compactionStatus=null,e.compactionClearTimer=null},vh))}function bh(e,t){if(!t)return;if(t.stream==="compaction"){mh(e,t);return}if(t.stream!=="tool")return;const n=typeof t.sessionKey=="string"?t.sessionKey:void 0;if(n&&n!==e.sessionKey||!n&&e.chatRunId&&t.runId!==e.chatRunId||e.chatRunId&&t.runId!==e.chatRunId||!e.chatRunId)return;const i=t.data??{},s=typeof i.toolCallId=="string"?i.toolCallId:"";if(!s)return;const a=typeof i.name=="string"?i.name:"tool",o=typeof i.phase=="string"?i.phase:"",l=o==="start"?i.args:void 0,d=o==="update"?Ha(i.partialResult):o==="result"?Ha(i.result):void 0,h=Date.now();let p=e.toolStreamById.get(s);p?(p.name=a,l!==void 0&&(p.args=l),d!==void 0&&(p.output=d||void 0),p.updatedAt=h):(p={toolCallId:s,runId:t.runId,sessionKey:n,name:a,args:l,output:d||void 0,startedAt:typeof t.ts=="number"?t.ts:h,updatedAt:h,message:{}},e.toolStreamById.set(s,p),e.toolStreamOrder.push(s)),p.message=fh(p),gh(e),ph(e,o==="result")}const yh=/^\[([^\]]+)\]\s*/,wh=["WebChat","WhatsApp","Telegram","Signal","Slack","Discord","iMessage","Teams","Matrix","Zalo","Zalo Personal","BlueBubbles"],pi=new WeakMap,vi=new WeakMap;function $h(e){return/\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z\b/.test(e)||/\d{4}-\d{2}-\d{2} \d{2}:\d{2}\b/.test(e)?!0:wh.some(t=>e.startsWith(`${t} `))}function mi(e){const t=e.match(yh);if(!t)return e;const n=t[1]??"";return $h(n)?e.slice(t[0].length):e}function Ki(e){const t=e,n=typeof t.role=="string"?t.role:"",i=t.content;if(typeof i=="string")return n==="assistant"?di(i):mi(i);if(Array.isArray(i)){const s=i.map(a=>{const o=a;return o.type==="text"&&typeof o.text=="string"?o.text:null}).filter(a=>typeof a=="string");if(s.length>0){const a=s.join(`
`);return n==="assistant"?di(a):mi(a)}}return typeof t.text=="string"?n==="assistant"?di(t.text):mi(t.text):null}function Ul(e){if(!e||typeof e!="object")return Ki(e);const t=e;if(pi.has(t))return pi.get(t)??null;const n=Ki(e);return pi.set(t,n),n}function ja(e){const n=e.content,i=[];if(Array.isArray(n))for(const l of n){const d=l;if(d.type==="thinking"&&typeof d.thinking=="string"){const h=d.thinking.trim();h&&i.push(h)}}if(i.length>0)return i.join(`
`);const s=Ah(e);if(!s)return null;const o=[...s.matchAll(/<\s*think(?:ing)?\s*>([\s\S]*?)<\s*\/\s*think(?:ing)?\s*>/gi)].map(l=>(l[1]??"").trim()).filter(Boolean);return o.length>0?o.join(`
`):null}function kh(e){if(!e||typeof e!="object")return ja(e);const t=e;if(vi.has(t))return vi.get(t)??null;const n=ja(e);return vi.set(t,n),n}function Ah(e){const t=e,n=t.content;if(typeof n=="string")return n;if(Array.isArray(n)){const i=n.map(s=>{const a=s;return a.type==="text"&&typeof a.text=="string"?a.text:null}).filter(s=>typeof s=="string");if(i.length>0)return i.join(`
`)}return typeof t.text=="string"?t.text:null}function Sh(e){const t=e.trim();if(!t)return"";const n=t.split(/\r?\n/).map(i=>i.trim()).filter(Boolean).map(i=>`_${i}_`);return n.length?["_Reasoning:_",...n].join(`
`):""}let Ga=!1;function Wa(e){e[6]=e[6]&15|64,e[8]=e[8]&63|128;let t="";for(let n=0;n<e.length;n++)t+=e[n].toString(16).padStart(2,"0");return`${t.slice(0,8)}-${t.slice(8,12)}-${t.slice(12,16)}-${t.slice(16,20)}-${t.slice(20)}`}function xh(){const e=new Uint8Array(16),t=Date.now();for(let n=0;n<e.length;n++)e[n]=Math.floor(Math.random()*256);return e[0]^=t&255,e[1]^=t>>>8&255,e[2]^=t>>>16&255,e[3]^=t>>>24&255,e}function _h(){Ga||(Ga=!0,console.warn("[uuid] crypto API missing; falling back to weak randomness"))}function Ls(e=globalThis.crypto){if(e&&typeof e.randomUUID=="function")return e.randomUUID();if(e&&typeof e.getRandomValues=="function"){const t=new Uint8Array(16);return e.getRandomValues(t),Wa(t)}return _h(),Wa(xh())}async function jt(e){if(!(!e.client||!e.connected)){e.chatLoading=!0,e.lastError=null;try{const t=await e.client.request("chat.history",{sessionKey:e.sessionKey,limit:200});e.chatMessages=Array.isArray(t.messages)?t.messages:[],e.chatThinkingLevel=t.thinkingLevel??null}catch(t){e.lastError=String(t)}finally{e.chatLoading=!1}}}function Ch(e){const t=/^data:([^;]+);base64,(.+)$/.exec(e);return t?{mimeType:t[1],content:t[2]}:null}async function Eh(e,t,n){if(!e.client||!e.connected)return null;const i=t.trim(),s=n&&n.length>0;if(!i&&!s)return null;const a=Date.now(),o=[];if(i&&o.push({type:"text",text:i}),s)for(const h of n)o.push({type:"image",source:{type:"base64",media_type:h.mimeType,data:h.dataUrl}});e.chatMessages=[...e.chatMessages,{role:"user",content:o,timestamp:a}],e.chatSending=!0,e.lastError=null;const l=Ls();e.chatRunId=l,e.chatStream="",e.chatStreamStartedAt=a;const d=s?n.map(h=>{const p=Ch(h.dataUrl);return p?{type:"image",mimeType:p.mimeType,content:p.content}:null}).filter(h=>h!==null):void 0;try{return await e.client.request("chat.send",{sessionKey:e.sessionKey,message:i,deliver:!1,idempotencyKey:l,attachments:d}),l}catch(h){const p=String(h);return e.chatRunId=null,e.chatStream=null,e.chatStreamStartedAt=null,e.lastError=p,e.chatMessages=[...e.chatMessages,{role:"assistant",content:[{type:"text",text:"Error: "+p}],timestamp:Date.now()}],null}finally{e.chatSending=!1}}async function Th(e){if(!e.client||!e.connected)return!1;const t=e.chatRunId;try{return await e.client.request("chat.abort",t?{sessionKey:e.sessionKey,runId:t}:{sessionKey:e.sessionKey}),!0}catch(n){return e.lastError=String(n),!1}}function Lh(e,t){if(!t||t.sessionKey!==e.sessionKey)return null;if(t.runId&&e.chatRunId&&t.runId!==e.chatRunId)return t.state==="final"?"final":null;if(t.state==="delta"){const n=Ki(t.message);if(typeof n=="string"){const i=e.chatStream??"";(!i||n.length>=i.length)&&(e.chatStream=n)}}else t.state==="final"||t.state==="aborted"?(e.chatStream=null,e.chatRunId=null,e.chatStreamStartedAt=null):t.state==="error"&&(e.chatStream=null,e.chatRunId=null,e.chatStreamStartedAt=null,e.lastError=t.errorMessage??"chat error");return t.state}const Kl=120;function zl(e){return e.chatSending||!!e.chatRunId}function Ih(e){const t=e.trim();if(!t)return!1;const n=t.toLowerCase();return n==="/stop"?!0:n==="stop"||n==="esc"||n==="abort"||n==="wait"||n==="exit"}function Rh(e){const t=e.trim();if(!t)return!1;const n=t.toLowerCase();return n==="/new"||n==="/reset"?!0:n.startsWith("/new ")||n.startsWith("/reset ")}async function Hl(e){e.connected&&(e.chatMessage="",await Th(e))}function Mh(e,t,n,i){const s=t.trim(),a=!!(n&&n.length>0);!s&&!a||(e.chatQueue=[...e.chatQueue,{id:Ls(),text:s,createdAt:Date.now(),attachments:a?n?.map(o=>({...o})):void 0,refreshSessions:i}])}async function jl(e,t,n){Hn(e);const i=await Eh(e,t,n?.attachments),s=!!i;return!s&&n?.previousDraft!=null&&(e.chatMessage=n.previousDraft),!s&&n?.previousAttachments&&(e.chatAttachments=n.previousAttachments),s&&Nl(e,e.sessionKey),s&&n?.restoreDraft&&n.previousDraft?.trim()&&(e.chatMessage=n.previousDraft),s&&n?.restoreAttachments&&n.previousAttachments?.length&&(e.chatAttachments=n.previousAttachments),Wt(e),s&&!e.chatRunId&&Gl(e),s&&n?.refreshSessions&&i&&e.refreshSessionsAfterChat.add(i),s}async function Gl(e){if(!e.connected||zl(e))return;const[t,...n]=e.chatQueue;if(!t)return;e.chatQueue=n,await jl(e,t.text,{attachments:t.attachments,refreshSessions:t.refreshSessions})||(e.chatQueue=[t,...e.chatQueue])}function Ph(e,t){e.chatQueue=e.chatQueue.filter(n=>n.id!==t)}async function Fh(e,t,n){if(!e.connected)return;const i=e.chatMessage,s=(t??e.chatMessage).trim(),a=e.chatAttachments??[],o=t==null?a:[],l=o.length>0;if(!s&&!l)return;if(Ih(s)){await Hl(e);return}const d=Rh(s);if(t==null&&(e.chatMessage="",e.chatAttachments=[]),zl(e)){Mh(e,s,o,d);return}await jl(e,s,{previousDraft:t==null?i:void 0,restoreDraft:!!(t&&n?.restoreDraft),attachments:l?o:void 0,previousAttachments:t==null?a:void 0,restoreAttachments:!!(t&&n?.restoreDraft),refreshSessions:d})}async function Wl(e){await Promise.all([jt(e),nt(e,{activeMinutes:Kl}),zi(e)]),Wt(e)}const Nh=Gl;function Oh(e){const t=ll(e.sessionKey);return t?.agentId?t.agentId:e.hello?.snapshot?.sessionDefaults?.defaultAgentId?.trim()||"main"}function Dh(e,t){const n=Yt(e),i=encodeURIComponent(t);return n?`${n}/avatar/${i}?meta=1`:`/avatar/${i}?meta=1`}async function zi(e){if(!e.connected){e.chatAvatarUrl=null;return}const t=Oh(e);if(!t){e.chatAvatarUrl=null;return}e.chatAvatarUrl=null;const n=Dh(e.basePath,t);try{const i=await fetch(n,{method:"GET"});if(!i.ok){e.chatAvatarUrl=null;return}const s=await i.json(),a=typeof s.avatarUrl=="string"?s.avatarUrl.trim():"";e.chatAvatarUrl=a||null}catch{e.chatAvatarUrl=null}}const Bh={trace:!0,debug:!0,info:!0,warn:!0,error:!0,fatal:!0},Uh={name:"",description:"",agentId:"",enabled:!0,scheduleKind:"every",scheduleAt:"",everyAmount:"30",everyUnit:"minutes",cronExpr:"0 7 * * *",cronTz:"",sessionTarget:"isolated",wakeMode:"next-heartbeat",payloadKind:"agentTurn",payloadText:"",deliveryMode:"announce",deliveryChannel:"last",deliveryTo:"",timeoutSeconds:""},Kh=50,zh=200,Hh="Assistant";function qa(e,t){if(typeof e!="string")return;const n=e.trim();if(n)return n.length<=t?n:n.slice(0,t)}function Hi(e){const t=qa(e?.name,Kh)??Hh,n=qa(e?.avatar??void 0,zh)??null;return{agentId:typeof e?.agentId=="string"&&e.agentId.trim()?e.agentId.trim():null,name:t,avatar:n}}function jh(){return Hi(typeof window>"u"?{}:{name:window.__OPENCLAW_ASSISTANT_NAME__,avatar:window.__OPENCLAW_ASSISTANT_AVATAR__})}async function ql(e,t){if(!e.client||!e.connected)return;const n=e.sessionKey.trim(),i=n?{sessionKey:n}:{};try{const s=await e.client.request("agent.identity.get",i);if(!s)return;const a=Hi(s);e.assistantName=a.name,e.assistantAvatar=a.avatar,e.assistantAgentId=a.agentId??null}catch{}}function ji(e){return typeof e=="object"&&e!==null}function Gh(e){if(!ji(e))return null;const t=typeof e.id=="string"?e.id.trim():"",n=e.request;if(!t||!ji(n))return null;const i=typeof n.command=="string"?n.command.trim():"";if(!i)return null;const s=typeof e.createdAtMs=="number"?e.createdAtMs:0,a=typeof e.expiresAtMs=="number"?e.expiresAtMs:0;return!s||!a?null:{id:t,request:{command:i,cwd:typeof n.cwd=="string"?n.cwd:null,host:typeof n.host=="string"?n.host:null,security:typeof n.security=="string"?n.security:null,ask:typeof n.ask=="string"?n.ask:null,agentId:typeof n.agentId=="string"?n.agentId:null,resolvedPath:typeof n.resolvedPath=="string"?n.resolvedPath:null,sessionKey:typeof n.sessionKey=="string"?n.sessionKey:null},createdAtMs:s,expiresAtMs:a}}function Wh(e){if(!ji(e))return null;const t=typeof e.id=="string"?e.id.trim():"";return t?{id:t,decision:typeof e.decision=="string"?e.decision:null,resolvedBy:typeof e.resolvedBy=="string"?e.resolvedBy:null,ts:typeof e.ts=="number"?e.ts:null}:null}function Vl(e){const t=Date.now();return e.filter(n=>n.expiresAtMs>t)}function qh(e,t){const n=Vl(e).filter(i=>i.id!==t.id);return n.push(t),n}function Va(e,t){return Vl(e).filter(n=>n.id!==t)}function Vh(e){const t=e.version??(e.nonce?"v2":"v1"),n=e.scopes.join(","),i=e.token??"",s=[t,e.deviceId,e.clientId,e.clientMode,e.role,n,String(e.signedAtMs),i];return t==="v2"&&s.push(e.nonce??""),s.join("|")}const Yl={WEBCHAT_UI:"webchat-ui",CONTROL_UI:"openclaw-control-ui",WEBCHAT:"webchat",CLI:"cli",GATEWAY_CLIENT:"gateway-client",MACOS_APP:"openclaw-macos",IOS_APP:"openclaw-ios",ANDROID_APP:"openclaw-android",NODE_HOST:"node-host",TEST:"test",FINGERPRINT:"fingerprint",PROBE:"openclaw-probe"},Ya=Yl,Gi={WEBCHAT:"webchat",CLI:"cli",UI:"ui",BACKEND:"backend",NODE:"node",PROBE:"probe",TEST:"test"};new Set(Object.values(Yl));new Set(Object.values(Gi));const Yh=4008;class Qh{constructor(t){this.opts=t,this.ws=null,this.pending=new Map,this.closed=!1,this.lastSeq=null,this.connectNonce=null,this.connectSent=!1,this.connectTimer=null,this.backoffMs=800}start(){this.closed=!1,this.connect()}stop(){this.closed=!0,this.ws?.close(),this.ws=null,this.flushPending(new Error("gateway client stopped"))}get connected(){return this.ws?.readyState===WebSocket.OPEN}connect(){this.closed||(this.ws=new WebSocket(this.opts.url),this.ws.addEventListener("open",()=>this.queueConnect()),this.ws.addEventListener("message",t=>this.handleMessage(String(t.data??""))),this.ws.addEventListener("close",t=>{const n=String(t.reason??"");this.ws=null,this.flushPending(new Error(`gateway closed (${t.code}): ${n}`)),this.opts.onClose?.({code:t.code,reason:n}),this.scheduleReconnect()}),this.ws.addEventListener("error",()=>{}))}scheduleReconnect(){if(this.closed)return;const t=this.backoffMs;this.backoffMs=Math.min(this.backoffMs*1.7,15e3),window.setTimeout(()=>this.connect(),t)}flushPending(t){for(const[,n]of this.pending)n.reject(t);this.pending.clear()}async sendConnect(){if(this.connectSent)return;this.connectSent=!0,this.connectTimer!==null&&(window.clearTimeout(this.connectTimer),this.connectTimer=null);const t=typeof crypto<"u"&&!!crypto.subtle,n=["operator.admin","operator.approvals","operator.pairing"],i="operator";let s=null,a=!1,o=this.opts.token;if(t){s=await Ss();const p=Xf({deviceId:s.deviceId,role:i})?.token;o=p??this.opts.token,a=!!(p&&this.opts.token)}const l=o||this.opts.password?{token:o,password:this.opts.password}:void 0;let d;if(t&&s){const p=Date.now(),u=this.connectNonce??void 0,y=Vh({deviceId:s.deviceId,clientId:this.opts.clientName??Ya.CONTROL_UI,clientMode:this.opts.mode??Gi.WEBCHAT,role:i,scopes:n,signedAtMs:p,token:o??null,nonce:u}),v=await Sg(s.privateKey,y);d={id:s.deviceId,publicKey:s.publicKey,signature:v,signedAt:p,nonce:u}}const h={minProtocol:3,maxProtocol:3,client:{id:this.opts.clientName??Ya.CONTROL_UI,version:this.opts.clientVersion??"dev",platform:this.opts.platform??navigator.platform??"web",mode:this.opts.mode??Gi.WEBCHAT,instanceId:this.opts.instanceId},role:i,scopes:n,device:d,caps:[],auth:l,userAgent:navigator.userAgent,locale:navigator.language};this.request("connect",h).then(p=>{p?.auth?.deviceToken&&s&&vl({deviceId:s.deviceId,role:p.auth.role??i,token:p.auth.deviceToken,scopes:p.auth.scopes??[]}),this.backoffMs=800,this.opts.onHello?.(p)}).catch(()=>{a&&s&&ml({deviceId:s.deviceId,role:i}),this.ws?.close(Yh,"connect failed")})}handleMessage(t){let n;try{n=JSON.parse(t)}catch{return}const i=n;if(i.type==="event"){const s=n;if(s.event==="connect.challenge"){const o=s.payload,l=o&&typeof o.nonce=="string"?o.nonce:null;l&&(this.connectNonce=l,this.sendConnect());return}const a=typeof s.seq=="number"?s.seq:null;a!==null&&(this.lastSeq!==null&&a>this.lastSeq+1&&this.opts.onGap?.({expected:this.lastSeq+1,received:a}),this.lastSeq=a);try{this.opts.onEvent?.(s)}catch(o){console.error("[gateway] event handler error:",o)}return}if(i.type==="res"){const s=n,a=this.pending.get(s.id);if(!a)return;this.pending.delete(s.id),s.ok?a.resolve(s.payload):a.reject(new Error(s.error?.message??"request failed"));return}}request(t,n){if(!this.ws||this.ws.readyState!==WebSocket.OPEN)return Promise.reject(new Error("gateway not connected"));const i=Ls(),s={type:"req",id:i,method:t,params:n},a=new Promise((o,l)=>{this.pending.set(i,{resolve:d=>o(d),reject:l})});return this.ws.send(JSON.stringify(s)),a}queueConnect(){this.connectNonce=null,this.connectSent=!1,this.connectTimer!==null&&window.clearTimeout(this.connectTimer),this.connectTimer=window.setTimeout(()=>{this.sendConnect()},750)}}function bi(e,t){const n=(e??"").trim(),i=t.mainSessionKey?.trim();if(!i)return n;if(!n)return i;const s=t.mainKey?.trim()||"main",a=t.defaultAgentId?.trim();return n==="main"||n===s||a&&(n===`agent:${a}:main`||n===`agent:${a}:${s}`)?i:n}function Jh(e,t){if(!t?.mainSessionKey)return;const n=bi(e.sessionKey,t),i=bi(e.settings.sessionKey,t),s=bi(e.settings.lastActiveSessionKey,t),a=n||i||e.sessionKey,o={...e.settings,sessionKey:i||a,lastActiveSessionKey:s||a},l=o.sessionKey!==e.settings.sessionKey||o.lastActiveSessionKey!==e.settings.lastActiveSessionKey;a!==e.sessionKey&&(e.sessionKey=a),l&&Oe(e,o)}function Ql(e){e.lastError=null,e.hello=null,e.connected=!1,e.execApprovalQueue=[],e.execApprovalError=null,e.client?.stop(),e.client=new Qh({url:e.settings.gatewayUrl,token:e.settings.token.trim()?e.settings.token:void 0,password:e.password.trim()?e.password:void 0,clientName:"openclaw-control-ui",mode:"webchat",onHello:t=>{e.connected=!0,e.lastError=null,e.hello=t,ep(e,t),e.chatRunId=null,e.chatStream=null,e.chatStreamStartedAt=null,Hn(e),ql(e),bs(e),Dn(e,{quiet:!0}),Be(e,{quiet:!0}),Ts(e)},onClose:({code:t,reason:n})=>{e.connected=!1,t!==1012&&(e.lastError=`disconnected (${t}): ${n||"no reason"}`)},onEvent:t=>Zh(e,t),onGap:({expected:t,received:n})=>{e.lastError=`event gap detected (expected seq ${t}, got ${n}); refresh recommended`}}),e.client.start()}function Zh(e,t){try{Xh(e,t)}catch(n){console.error("[gateway] handleGatewayEvent error:",t.event,n)}}function Xh(e,t){if(e.eventLogBuffer=[{ts:Date.now(),event:t.event,payload:t.payload},...e.eventLogBuffer].slice(0,250),e.tab==="debug"&&(e.eventLog=e.eventLogBuffer),t.event==="agent"){if(e.onboarding)return;bh(e,t.payload);return}if(t.event==="chat"){const n=t.payload;n?.sessionKey&&Nl(e,n.sessionKey);const i=Lh(e,n);if(i==="final"||i==="error"||i==="aborted"){Hn(e),Nh(e);const s=n?.runId;s&&e.refreshSessionsAfterChat.has(s)&&(e.refreshSessionsAfterChat.delete(s),i==="final"&&nt(e,{activeMinutes:Kl}))}i==="final"&&jt(e);return}if(t.event==="presence"){const n=t.payload;n?.presence&&Array.isArray(n.presence)&&(e.presenceEntries=n.presence,e.presenceError=null,e.presenceStatus=null);return}if(t.event==="cron"&&e.tab==="cron"&&Tn(e),(t.event==="device.pair.requested"||t.event==="device.pair.resolved")&&Be(e,{quiet:!0}),t.event==="exec.approval.requested"){const n=Gh(t.payload);if(n){e.execApprovalQueue=qh(e.execApprovalQueue,n),e.execApprovalError=null;const i=Math.max(0,n.expiresAtMs-Date.now()+500);window.setTimeout(()=>{e.execApprovalQueue=Va(e.execApprovalQueue,n.id)},i)}return}if(t.event==="exec.approval.resolved"){const n=Wh(t.payload);n&&(e.execApprovalQueue=Va(e.execApprovalQueue,n.id))}}function ep(e,t){const n=t.snapshot;n?.presence&&Array.isArray(n.presence)&&(e.presenceEntries=n.presence),n?.health&&(e.debugHealth=n.health),n?.sessionDefaults&&Jh(e,n.sessionDefaults)}function tp(e){e.basePath=th(),Zg(e),ah(e,!0),nh(e),ih(e),window.addEventListener("popstate",e.popStateHandler),Ql(e),Kf(e),e.tab==="logs"&&hs(e),e.tab==="debug"&&vs(e)}function np(e){Pf(e)}function ip(e){window.removeEventListener("popstate",e.popStateHandler),zf(e),ps(e),ms(e),sh(e),e.topbarObserver?.disconnect(),e.topbarObserver=null}function sp(e,t){if(e.tab==="chat"&&(t.has("chatMessages")||t.has("chatToolMessages")||t.has("chatStream")||t.has("chatLoading")||t.has("tab"))){const n=t.has("tab"),i=t.has("chatLoading")&&t.get("chatLoading")===!0&&!e.chatLoading;Wt(e,n||i||!e.chatHasAutoScrolled)}e.tab==="logs"&&(t.has("logsEntries")||t.has("logsAutoFollow")||t.has("tab"))&&e.logsAutoFollow&&e.logsAtBottom&&rl(e,t.has("tab")||t.has("logsAutoFollow"))}const Is={CHILD:2},Rs=e=>(...t)=>({_$litDirective$:e,values:t});let Ms=class{constructor(t){}get _$AU(){return this._$AM._$AU}_$AT(t,n,i){this._$Ct=t,this._$AM=n,this._$Ci=i}_$AS(t,n){return this.update(t,n)}update(t,n){return this.render(...n)}};const{I:ap}=nf,Qa=e=>e,op=e=>e.strings===void 0,Ja=()=>document.createComment(""),$t=(e,t,n)=>{const i=e._$AA.parentNode,s=t===void 0?e._$AB:t._$AA;if(n===void 0){const a=i.insertBefore(Ja(),s),o=i.insertBefore(Ja(),s);n=new ap(a,o,e,e.options)}else{const a=n._$AB.nextSibling,o=n._$AM,l=o!==e;if(l){let d;n._$AQ?.(e),n._$AM=e,n._$AP!==void 0&&(d=e._$AU)!==o._$AU&&n._$AP(d)}if(a!==s||l){let d=n._$AA;for(;d!==a;){const h=Qa(d).nextSibling;Qa(i).insertBefore(d,s),d=h}}}return n},je=(e,t,n=e)=>(e._$AI(t,n),e),lp={},rp=(e,t=lp)=>e._$AH=t,cp=e=>e._$AH,yi=e=>{e._$AR(),e._$AA.remove()};const Za=(e,t,n)=>{const i=new Map;for(let s=t;s<=n;s++)i.set(e[s],s);return i},Jl=Rs(class extends Ms{constructor(e){if(super(e),e.type!==Is.CHILD)throw Error("repeat() can only be used in text expressions")}dt(e,t,n){let i;n===void 0?n=t:t!==void 0&&(i=t);const s=[],a=[];let o=0;for(const l of e)s[o]=i?i(l,o):o,a[o]=n(l,o),o++;return{values:a,keys:s}}render(e,t,n){return this.dt(e,t,n).values}update(e,[t,n,i]){const s=cp(e),{values:a,keys:o}=this.dt(t,n,i);if(!Array.isArray(s))return this.ut=o,a;const l=this.ut??=[],d=[];let h,p,u=0,y=s.length-1,v=0,$=a.length-1;for(;u<=y&&v<=$;)if(s[u]===null)u++;else if(s[y]===null)y--;else if(l[u]===o[v])d[v]=je(s[u],a[v]),u++,v++;else if(l[y]===o[$])d[$]=je(s[y],a[$]),y--,$--;else if(l[u]===o[$])d[$]=je(s[u],a[$]),$t(e,d[$+1],s[u]),u++,$--;else if(l[y]===o[v])d[v]=je(s[y],a[v]),$t(e,s[u],s[y]),y--,v++;else if(h===void 0&&(h=Za(o,v,$),p=Za(l,u,y)),h.has(l[u]))if(h.has(l[y])){const g=p.get(o[v]),w=g!==void 0?s[g]:null;if(w===null){const _=$t(e,s[u]);je(_,a[v]),d[v]=_}else d[v]=je(w,a[v]),$t(e,s[u],w),s[g]=null;v++}else yi(s[y]),y--;else yi(s[u]),u++;for(;v<=$;){const g=$t(e,d[$+1]);je(g,a[v]),d[v++]=g}for(;u<=y;){const g=s[u++];g!==null&&yi(g)}return this.ut=o,rp(e,d),Ne}}),J={messageSquare:r`
    <svg viewBox="0 0 24 24">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  `,barChart:r`
    <svg viewBox="0 0 24 24">
      <line x1="12" x2="12" y1="20" y2="10" />
      <line x1="18" x2="18" y1="20" y2="4" />
      <line x1="6" x2="6" y1="20" y2="16" />
    </svg>
  `,link:r`
    <svg viewBox="0 0 24 24">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
    </svg>
  `,radio:r`
    <svg viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="2" />
      <path
        d="M16.24 7.76a6 6 0 0 1 0 8.49m-8.48-.01a6 6 0 0 1 0-8.49m11.31-2.82a10 10 0 0 1 0 14.14m-14.14 0a10 10 0 0 1 0-14.14"
      />
    </svg>
  `,fileText:r`
    <svg viewBox="0 0 24 24">
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" x2="8" y1="13" y2="13" />
      <line x1="16" x2="8" y1="17" y2="17" />
      <line x1="10" x2="8" y1="9" y2="9" />
    </svg>
  `,zap:r`
    <svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></svg>
  `,monitor:r`
    <svg viewBox="0 0 24 24">
      <rect width="20" height="14" x="2" y="3" rx="2" />
      <line x1="8" x2="16" y1="21" y2="21" />
      <line x1="12" x2="12" y1="17" y2="21" />
    </svg>
  `,settings:r`
    <svg viewBox="0 0 24 24">
      <path
        d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"
      />
      <circle cx="12" cy="12" r="3" />
    </svg>
  `,bug:r`
    <svg viewBox="0 0 24 24">
      <path d="m8 2 1.88 1.88" />
      <path d="M14.12 3.88 16 2" />
      <path d="M9 7.13v-1a3.003 3.003 0 1 1 6 0v1" />
      <path d="M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6" />
      <path d="M12 20v-9" />
      <path d="M6.53 9C4.6 8.8 3 7.1 3 5" />
      <path d="M6 13H2" />
      <path d="M3 21c0-2.1 1.7-3.9 3.8-4" />
      <path d="M20.97 5c0 2.1-1.6 3.8-3.5 4" />
      <path d="M22 13h-4" />
      <path d="M17.2 17c2.1.1 3.8 1.9 3.8 4" />
    </svg>
  `,scrollText:r`
    <svg viewBox="0 0 24 24">
      <path d="M8 21h12a2 2 0 0 0 2-2v-2H10v2a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v3h4" />
      <path d="M19 17V5a2 2 0 0 0-2-2H4" />
      <path d="M15 8h-5" />
      <path d="M15 12h-5" />
    </svg>
  `,folder:r`
    <svg viewBox="0 0 24 24">
      <path
        d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"
      />
    </svg>
  `,menu:r`
    <svg viewBox="0 0 24 24">
      <line x1="4" x2="20" y1="12" y2="12" />
      <line x1="4" x2="20" y1="6" y2="6" />
      <line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  `,x:r`
    <svg viewBox="0 0 24 24">
      <path d="M18 6 6 18" />
      <path d="m6 6 12 12" />
    </svg>
  `,check:r`
    <svg viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5" /></svg>
  `,arrowDown:r`
    <svg viewBox="0 0 24 24">
      <path d="M12 5v14" />
      <path d="m19 12-7 7-7-7" />
    </svg>
  `,copy:r`
    <svg viewBox="0 0 24 24">
      <rect width="14" height="14" x="8" y="8" rx="2" ry="2" />
      <path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />
    </svg>
  `,search:r`
    <svg viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  `,brain:r`
    <svg viewBox="0 0 24 24">
      <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" />
      <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z" />
      <path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4" />
      <path d="M17.599 6.5a3 3 0 0 0 .399-1.375" />
      <path d="M6.003 5.125A3 3 0 0 0 6.401 6.5" />
      <path d="M3.477 10.896a4 4 0 0 1 .585-.396" />
      <path d="M19.938 10.5a4 4 0 0 1 .585.396" />
      <path d="M6 18a4 4 0 0 1-1.967-.516" />
      <path d="M19.967 17.484A4 4 0 0 1 18 18" />
    </svg>
  `,book:r`
    <svg viewBox="0 0 24 24">
      <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
    </svg>
  `,loader:r`
    <svg viewBox="0 0 24 24">
      <path d="M12 2v4" />
      <path d="m16.2 7.8 2.9-2.9" />
      <path d="M18 12h4" />
      <path d="m16.2 16.2 2.9 2.9" />
      <path d="M12 18v4" />
      <path d="m4.9 19.1 2.9-2.9" />
      <path d="M2 12h4" />
      <path d="m4.9 4.9 2.9 2.9" />
    </svg>
  `,wrench:r`
    <svg viewBox="0 0 24 24">
      <path
        d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
      />
    </svg>
  `,fileCode:r`
    <svg viewBox="0 0 24 24">
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <polyline points="14 2 14 8 20 8" />
      <path d="m10 13-2 2 2 2" />
      <path d="m14 17 2-2-2-2" />
    </svg>
  `,edit:r`
    <svg viewBox="0 0 24 24">
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
    </svg>
  `,penLine:r`
    <svg viewBox="0 0 24 24">
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
    </svg>
  `,paperclip:r`
    <svg viewBox="0 0 24 24">
      <path
        d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"
      />
    </svg>
  `,globe:r`
    <svg viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" />
      <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20" />
      <path d="M2 12h20" />
    </svg>
  `,image:r`
    <svg viewBox="0 0 24 24">
      <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
      <circle cx="9" cy="9" r="2" />
      <path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
    </svg>
  `,smartphone:r`
    <svg viewBox="0 0 24 24">
      <rect width="14" height="20" x="5" y="2" rx="2" ry="2" />
      <path d="M12 18h.01" />
    </svg>
  `,plug:r`
    <svg viewBox="0 0 24 24">
      <path d="M12 22v-5" />
      <path d="M9 8V2" />
      <path d="M15 8V2" />
      <path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z" />
    </svg>
  `,circle:r`
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /></svg>
  `,puzzle:r`
    <svg viewBox="0 0 24 24">
      <path
        d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.61a2.404 2.404 0 0 1-1.705.707 2.402 2.402 0 0 1-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.402 2.402 0 0 1 1.998 12c0-.617.236-1.234.706-1.704L4.23 8.77c.24-.24.581-.353.917-.303.515.076.874.54 1.02 1.02a2.5 2.5 0 1 0 3.237-3.237c-.48-.146-.944-.505-1.02-1.02a.98.98 0 0 1 .303-.917l1.526-1.526A2.402 2.402 0 0 1 11.998 2c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968a2.5 2.5 0 1 1 3.236 3.236c-.464.18-.894.527-.967 1.02Z"
      />
    </svg>
  `};function dp(e,t){const n=Cs(t,e.basePath);return r`
    <a
      href=${n}
      class="nav-item ${e.tab===t?"active":""}"
      @click=${i=>{i.defaultPrevented||i.button!==0||i.metaKey||i.ctrlKey||i.shiftKey||i.altKey||(i.preventDefault(),e.setTab(t))}}
      title=${Bi(t)}
    >
      <span class="nav-item__icon" aria-hidden="true">${J[Hg(t)]}</span>
      <span class="nav-item__text">${Bi(t)}</span>
    </a>
  `}function up(e){const t=fp(e.hello,e.sessionsResult),n=gp(e.sessionKey,e.sessionsResult,t),i=e.onboarding,s=e.onboarding,a=e.onboarding?!1:e.settings.chatShowThinking,o=e.onboarding?!0:e.settings.chatFocusMode,l=r`
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"></path>
      <path d="M21 3v5h-5"></path>
    </svg>
  `,d=r`
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M4 7V4h3"></path>
      <path d="M20 7V4h-3"></path>
      <path d="M4 17v3h3"></path>
      <path d="M20 17v3h-3"></path>
      <circle cx="12" cy="12" r="3"></circle>
    </svg>
  `;return r`
    <div class="chat-controls">
      <label class="field chat-controls__session">
        <select
          .value=${e.sessionKey}
          ?disabled=${!e.connected}
          @change=${h=>{const p=h.target.value;e.sessionKey=p,e.chatMessage="",e.chatStream=null,e.chatStreamStartedAt=null,e.chatRunId=null,e.resetToolStream(),e.resetChatScroll(),e.applySettings({...e.settings,sessionKey:p,lastActiveSessionKey:p}),e.loadAssistantIdentity(),lh(p),jt(e)}}
        >
          ${Jl(n,h=>h.key,h=>r`<option value=${h.key}>
                ${h.displayName??h.key}
              </option>`)}
        </select>
      </label>
      <button
        class="btn btn--sm btn--icon"
        ?disabled=${e.chatLoading||!e.connected}
        @click=${()=>{e.resetToolStream(),Wl(e)}}
        title="Refresh chat data"
      >
        ${l}
      </button>
      <span class="chat-controls__separator">|</span>
      <button
        class="btn btn--sm btn--icon ${a?"active":""}"
        ?disabled=${i}
        @click=${()=>{i||e.applySettings({...e.settings,chatShowThinking:!e.settings.chatShowThinking})}}
        aria-pressed=${a}
        title=${i?"Disabled during onboarding":"Toggle assistant thinking/working output"}
      >
        ${J.brain}
      </button>
      <button
        class="btn btn--sm btn--icon ${o?"active":""}"
        ?disabled=${s}
        @click=${()=>{s||e.applySettings({...e.settings,chatFocusMode:!e.settings.chatFocusMode})}}
        aria-pressed=${o}
        title=${s?"Disabled during onboarding":"Toggle focus mode (hide sidebar + page header)"}
      >
        ${d}
      </button>
    </div>
  `}function fp(e,t){const n=e?.snapshot,i=n?.sessionDefaults?.mainSessionKey?.trim();if(i)return i;const s=n?.sessionDefaults?.mainKey?.trim();return s||(t?.sessions?.some(a=>a.key==="main")?"main":null)}function wi(e,t){const n=t?.label?.trim();if(n)return`${n} (${e})`;const i=t?.displayName?.trim();return i||e}function gp(e,t,n){const i=new Set,s=[],a=n&&t?.sessions?.find(l=>l.key===n),o=t?.sessions?.find(l=>l.key===e);if(n&&(i.add(n),s.push({key:n,displayName:wi(n,a||void 0)})),i.has(e)||(i.add(e),s.push({key:e,displayName:wi(e,o)})),t?.sessions)for(const l of t.sessions)i.has(l.key)||(i.add(l.key),s.push({key:l.key,displayName:wi(l.key,l)}));return s}const hp=["system","light","dark"];function pp(e){const t=Math.max(0,hp.indexOf(e.theme)),n=i=>s=>{const o={element:s.currentTarget};(s.clientX||s.clientY)&&(o.pointerClientX=s.clientX,o.pointerClientY=s.clientY),e.setTheme(i,o)};return r`
    <div class="theme-toggle" style="--theme-index: ${t};">
      <div class="theme-toggle__track" role="group" aria-label="Theme">
        <span class="theme-toggle__indicator"></span>
        <button
          class="theme-toggle__button ${e.theme==="system"?"active":""}"
          @click=${n("system")}
          aria-pressed=${e.theme==="system"}
          aria-label="System theme"
          title="System"
        >
          ${bp()}
        </button>
        <button
          class="theme-toggle__button ${e.theme==="light"?"active":""}"
          @click=${n("light")}
          aria-pressed=${e.theme==="light"}
          aria-label="Light theme"
          title="Light"
        >
          ${vp()}
        </button>
        <button
          class="theme-toggle__button ${e.theme==="dark"?"active":""}"
          @click=${n("dark")}
          aria-pressed=${e.theme==="dark"}
          aria-label="Dark theme"
          title="Dark"
        >
          ${mp()}
        </button>
      </div>
    </div>
  `}function vp(){return r`
    <svg class="theme-icon" viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="4"></circle>
      <path d="M12 2v2"></path>
      <path d="M12 20v2"></path>
      <path d="m4.93 4.93 1.41 1.41"></path>
      <path d="m17.66 17.66 1.41 1.41"></path>
      <path d="M2 12h2"></path>
      <path d="M20 12h2"></path>
      <path d="m6.34 17.66-1.41 1.41"></path>
      <path d="m19.07 4.93-1.41 1.41"></path>
    </svg>
  `}function mp(){return r`
    <svg class="theme-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path
        d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"
      ></path>
    </svg>
  `}function bp(){return r`
    <svg class="theme-icon" viewBox="0 0 24 24" aria-hidden="true">
      <rect width="20" height="14" x="2" y="3" rx="2"></rect>
      <line x1="8" x2="16" y1="21" y2="21"></line>
      <line x1="12" x2="12" y1="17" y2="21"></line>
    </svg>
  `}function Zl(e,t){if(!e)return e;const i=e.files.some(s=>s.name===t.name)?e.files.map(s=>s.name===t.name?t:s):[...e.files,t];return{...e,files:i}}async function $i(e,t){if(!(!e.client||!e.connected||e.agentFilesLoading)){e.agentFilesLoading=!0,e.agentFilesError=null;try{const n=await e.client.request("agents.files.list",{agentId:t});n&&(e.agentFilesList=n,e.agentFileActive&&!n.files.some(i=>i.name===e.agentFileActive)&&(e.agentFileActive=null))}catch(n){e.agentFilesError=String(n)}finally{e.agentFilesLoading=!1}}}async function Xa(e,t,n,i){if(!(!e.client||!e.connected||e.agentFilesLoading)&&!(!i?.force&&Object.hasOwn(e.agentFileContents,n))){e.agentFilesLoading=!0,e.agentFilesError=null;try{const s=await e.client.request("agents.files.get",{agentId:t,name:n});if(s?.file){const a=s.file.content??"",o=e.agentFileContents[n]??"",l=e.agentFileDrafts[n],d=i?.preserveDraft??!0;e.agentFilesList=Zl(e.agentFilesList,s.file),e.agentFileContents={...e.agentFileContents,[n]:a},(!d||!Object.hasOwn(e.agentFileDrafts,n)||l===o)&&(e.agentFileDrafts={...e.agentFileDrafts,[n]:a})}}catch(s){e.agentFilesError=String(s)}finally{e.agentFilesLoading=!1}}}async function yp(e,t,n,i){if(!(!e.client||!e.connected||e.agentFileSaving)){e.agentFileSaving=!0,e.agentFilesError=null;try{const s=await e.client.request("agents.files.set",{agentId:t,name:n,content:i});s?.file&&(e.agentFilesList=Zl(e.agentFilesList,s.file),e.agentFileContents={...e.agentFileContents,[n]:i},e.agentFileDrafts={...e.agentFileDrafts,[n]:i})}catch(s){e.agentFilesError=String(s)}finally{e.agentFileSaving=!1}}}const wp={bash:"exec","apply-patch":"apply_patch"},$p={"group:memory":["memory_search","memory_get"],"group:web":["web_search","web_fetch"],"group:fs":["read","write","edit","apply_patch"],"group:runtime":["exec","process"],"group:sessions":["sessions_list","sessions_history","sessions_send","sessions_spawn","session_status"],"group:ui":["browser","canvas"],"group:automation":["cron","gateway"],"group:messaging":["message"],"group:nodes":["nodes"],"group:openclaw":["browser","canvas","nodes","cron","message","gateway","agents_list","sessions_list","sessions_history","sessions_send","sessions_spawn","session_status","memory_search","memory_get","web_search","web_fetch","image"]},kp={minimal:{allow:["session_status"]},coding:{allow:["group:fs","group:runtime","group:sessions","group:memory","image"]},messaging:{allow:["group:messaging","sessions_list","sessions_history","sessions_send","session_status"]},full:{}};function Ae(e){const t=e.trim().toLowerCase();return wp[t]??t}function Ap(e){return e?e.map(Ae).filter(Boolean):[]}function Sp(e){const t=Ap(e),n=[];for(const i of t){const s=$p[i];if(s){n.push(...s);continue}n.push(i)}return Array.from(new Set(n))}function xp(e){if(!e)return;const t=kp[e];if(t&&!(!t.allow&&!t.deny))return{allow:t.allow?[...t.allow]:void 0,deny:t.deny?[...t.deny]:void 0}}function _p(e){const t=e.host??"unknown",n=e.ip?`(${e.ip})`:"",i=e.mode??"",s=e.version??"";return`${t} ${n} ${i} ${s}`.trim()}function Cp(e){const t=e.ts??null;return t?U(t):"n/a"}function Ps(e){return e?`${Kt(e)} (${U(e)})`:"n/a"}function Ep(e){if(e.totalTokens==null)return"n/a";const t=e.totalTokens??0,n=e.contextTokens??0;return n?`${t} / ${n}`:String(t)}function Tp(e){if(e==null)return"";try{return JSON.stringify(e,null,2)}catch{return String(e)}}function Xl(e){const t=e.state??{},n=t.nextRunAtMs?Kt(t.nextRunAtMs):"n/a",i=t.lastRunAtMs?Kt(t.lastRunAtMs):"n/a";return`${t.lastStatus??"n/a"} · next ${n} · last ${i}`}function er(e){const t=e.schedule;if(t.kind==="at"){const n=Date.parse(t.at);return Number.isFinite(n)?`At ${Kt(n)}`:`At ${t.at}`}return t.kind==="every"?`Every ${ul(t.everyMs)}`:`Cron ${t.expr}${t.tz?` (${t.tz})`:""}`}function tr(e){const t=e.payload;if(t.kind==="systemEvent")return`System: ${t.text}`;const n=`Agent: ${t.message}`,i=e.delivery;if(i&&i.mode!=="none"){const s=i.channel||i.to?` (${i.channel??"last"}${i.to?` -> ${i.to}`:""})`:"";return`${n} · ${i.mode}${s}`}return n}const eo=[{id:"fs",label:"Files",tools:[{id:"read",label:"read",description:"Read file contents"},{id:"write",label:"write",description:"Create or overwrite files"},{id:"edit",label:"edit",description:"Make precise edits"},{id:"apply_patch",label:"apply_patch",description:"Patch files (OpenAI)"}]},{id:"runtime",label:"Runtime",tools:[{id:"exec",label:"exec",description:"Run shell commands"},{id:"process",label:"process",description:"Manage background processes"}]},{id:"web",label:"Web",tools:[{id:"web_search",label:"web_search",description:"Search the web"},{id:"web_fetch",label:"web_fetch",description:"Fetch web content"}]},{id:"memory",label:"Memory",tools:[{id:"memory_search",label:"memory_search",description:"Semantic search"},{id:"memory_get",label:"memory_get",description:"Read memory files"}]},{id:"sessions",label:"Sessions",tools:[{id:"sessions_list",label:"sessions_list",description:"List sessions"},{id:"sessions_history",label:"sessions_history",description:"Session history"},{id:"sessions_send",label:"sessions_send",description:"Send to session"},{id:"sessions_spawn",label:"sessions_spawn",description:"Spawn sub-agent"},{id:"session_status",label:"session_status",description:"Session status"}]},{id:"ui",label:"UI",tools:[{id:"browser",label:"browser",description:"Control web browser"},{id:"canvas",label:"canvas",description:"Control canvases"}]},{id:"messaging",label:"Messaging",tools:[{id:"message",label:"message",description:"Send messages"}]},{id:"automation",label:"Automation",tools:[{id:"cron",label:"cron",description:"Schedule tasks"},{id:"gateway",label:"gateway",description:"Gateway control"}]},{id:"nodes",label:"Nodes",tools:[{id:"nodes",label:"nodes",description:"Nodes + devices"}]},{id:"agents",label:"Agents",tools:[{id:"agents_list",label:"agents_list",description:"List agents"}]},{id:"media",label:"Media",tools:[{id:"image",label:"image",description:"Image understanding"}]}],Lp=[{id:"minimal",label:"Minimal"},{id:"coding",label:"Coding"},{id:"messaging",label:"Messaging"},{id:"full",label:"Full"}];function Wi(e){return e.name?.trim()||e.identity?.name?.trim()||e.id}function un(e){const t=e.trim();if(!t||t.length>16)return!1;let n=!1;for(let i=0;i<t.length;i+=1)if(t.charCodeAt(i)>127){n=!0;break}return!(!n||t.includes("://")||t.includes("/")||t.includes("."))}function jn(e,t){const n=t?.emoji?.trim();if(n&&un(n))return n;const i=e.identity?.emoji?.trim();if(i&&un(i))return i;const s=t?.avatar?.trim();if(s&&un(s))return s;const a=e.identity?.avatar?.trim();return a&&un(a)?a:""}function nr(e,t){return t&&e===t?"default":null}function Ip(e){if(e==null||!Number.isFinite(e))return"-";if(e<1024)return`${e} B`;const t=["KB","MB","GB","TB"];let n=e/1024,i=0;for(;n>=1024&&i<t.length-1;)n/=1024,i+=1;return`${n.toFixed(n<10?1:0)} ${t[i]}`}function Gn(e,t){const n=e;return{entry:(n?.agents?.list??[]).find(a=>a?.id===t),defaults:n?.agents?.defaults,globalTools:n?.tools}}function ir(e,t,n,i,s){const a=Gn(t,e.id),l=(n&&n.agentId===e.id?n.workspace:null)||a.entry?.workspace||a.defaults?.workspace||"default",d=a.entry?.model?Pt(a.entry?.model):Pt(a.defaults?.model),h=s?.name?.trim()||e.identity?.name?.trim()||e.name?.trim()||a.entry?.name||e.id,p=jn(e,s)||"-",u=Array.isArray(a.entry?.skills)?a.entry?.skills:null,y=u?.length??null;return{workspace:l,model:d,identityName:h,identityEmoji:p,skillsLabel:u?`${y} selected`:"all skills",isDefault:!!(i&&e.id===i)}}function Pt(e){if(!e)return"-";if(typeof e=="string")return e.trim()||"-";if(typeof e=="object"&&e){const t=e,n=t.primary?.trim();if(n){const i=Array.isArray(t.fallbacks)?t.fallbacks.length:0;return i>0?`${n} (+${i} fallback)`:n}}return"-"}function to(e){const t=e.match(/^(.+) \(\+\d+ fallback\)$/);return t?t[1]:e}function no(e){if(!e)return null;if(typeof e=="string")return e.trim()||null;if(typeof e=="object"&&e){const t=e;return(typeof t.primary=="string"?t.primary:typeof t.model=="string"?t.model:typeof t.id=="string"?t.id:typeof t.value=="string"?t.value:null)?.trim()||null}return null}function Rp(e){if(!e||typeof e=="string")return null;if(typeof e=="object"&&e){const t=e,n=Array.isArray(t.fallbacks)?t.fallbacks:Array.isArray(t.fallback)?t.fallback:null;return n?n.filter(i=>typeof i=="string"):null}return null}function Mp(e){return e.split(",").map(t=>t.trim()).filter(Boolean)}function Pp(e){const n=e?.agents?.defaults?.models;if(!n||typeof n!="object")return[];const i=[];for(const[s,a]of Object.entries(n)){const o=s.trim();if(!o)continue;const l=a&&typeof a=="object"&&"alias"in a&&typeof a.alias=="string"?a.alias?.trim():void 0,d=l&&l!==o?`${l} (${o})`:o;i.push({value:o,label:d})}return i}function Fp(e,t){const n=Pp(e),i=t?n.some(s=>s.value===t):!1;return t&&!i&&n.unshift({value:t,label:`Current (${t})`}),n.length===0?r`
      <option value="" disabled>No configured models</option>
    `:n.map(s=>r`<option value=${s.value}>${s.label}</option>`)}function Np(e){const t=Ae(e);if(!t)return{kind:"exact",value:""};if(t==="*")return{kind:"all"};if(!t.includes("*"))return{kind:"exact",value:t};const n=t.replace(/[.*+?^${}()|[\\]\\]/g,"\\$&");return{kind:"regex",value:new RegExp(`^${n.replaceAll("\\*",".*")}$`)}}function qi(e){return Array.isArray(e)?Sp(e).map(Np).filter(t=>t.kind!=="exact"||t.value.length>0):[]}function Ft(e,t){for(const n of t)if(n.kind==="all"||n.kind==="exact"&&e===n.value||n.kind==="regex"&&n.value.test(e))return!0;return!1}function Op(e,t){if(!t)return!0;const n=Ae(e),i=qi(t.deny);if(Ft(n,i))return!1;const s=qi(t.allow);return!!(s.length===0||Ft(n,s)||n==="apply_patch"&&Ft("exec",s))}function io(e,t){if(!Array.isArray(t)||t.length===0)return!1;const n=Ae(e),i=qi(t);return!!(Ft(n,i)||n==="apply_patch"&&Ft("exec",i))}function Dp(e){const t=e.agentsList?.agents??[],n=e.agentsList?.defaultId??null,i=e.selectedAgentId??n??t[0]?.id??null,s=i?t.find(a=>a.id===i)??null:null;return r`
    <div class="agents-layout">
      <section class="card agents-sidebar">
        <div class="row" style="justify-content: space-between;">
          <div>
            <div class="card-title">Agents</div>
            <div class="card-sub">${t.length} configured.</div>
          </div>
          <button class="btn btn--sm" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Loading…":"Refresh"}
          </button>
        </div>
        ${e.error?r`<div class="callout danger" style="margin-top: 12px;">${e.error}</div>`:m}
        <div class="agent-list" style="margin-top: 12px;">
          ${t.length===0?r`
                  <div class="muted">No agents found.</div>
                `:t.map(a=>{const o=nr(a.id,n),l=jn(a,e.agentIdentityById[a.id]??null);return r`
                    <button
                      type="button"
                      class="agent-row ${i===a.id?"active":""}"
                      @click=${()=>e.onSelectAgent(a.id)}
                    >
                      <div class="agent-avatar">
                        ${l||Wi(a).slice(0,1)}
                      </div>
                      <div class="agent-info">
                        <div class="agent-title">${Wi(a)}</div>
                        <div class="agent-sub mono">${a.id}</div>
                      </div>
                      ${o?r`<span class="agent-pill">${o}</span>`:m}
                    </button>
                  `})}
        </div>
      </section>
      <section class="agents-main">
        ${s?r`
              ${Bp(s,n,e.agentIdentityById[s.id]??null)}
              ${Up(e.activePanel,a=>e.onSelectPanel(a))}
              ${e.activePanel==="overview"?Kp({agent:s,defaultId:n,configForm:e.configForm,agentFilesList:e.agentFilesList,agentIdentity:e.agentIdentityById[s.id]??null,agentIdentityError:e.agentIdentityError,agentIdentityLoading:e.agentIdentityLoading,configLoading:e.configLoading,configSaving:e.configSaving,configDirty:e.configDirty,onConfigReload:e.onConfigReload,onConfigSave:e.onConfigSave,onModelChange:e.onModelChange,onModelFallbacksChange:e.onModelFallbacksChange}):m}
              ${e.activePanel==="files"?Jp({agentId:s.id,agentFilesList:e.agentFilesList,agentFilesLoading:e.agentFilesLoading,agentFilesError:e.agentFilesError,agentFileActive:e.agentFileActive,agentFileContents:e.agentFileContents,agentFileDrafts:e.agentFileDrafts,agentFileSaving:e.agentFileSaving,onLoadFiles:e.onLoadFiles,onSelectFile:e.onSelectFile,onFileDraftChange:e.onFileDraftChange,onFileReset:e.onFileReset,onFileSave:e.onFileSave}):m}
              ${e.activePanel==="tools"?Xp({agentId:s.id,configForm:e.configForm,configLoading:e.configLoading,configSaving:e.configSaving,configDirty:e.configDirty,onProfileChange:e.onToolsProfileChange,onOverridesChange:e.onToolsOverridesChange,onConfigReload:e.onConfigReload,onConfigSave:e.onConfigSave}):m}
              ${e.activePanel==="skills"?tv({agentId:s.id,report:e.agentSkillsReport,loading:e.agentSkillsLoading,error:e.agentSkillsError,activeAgentId:e.agentSkillsAgentId,configForm:e.configForm,configLoading:e.configLoading,configSaving:e.configSaving,configDirty:e.configDirty,filter:e.skillsFilter,onFilterChange:e.onSkillsFilterChange,onRefresh:e.onSkillsRefresh,onToggle:e.onAgentSkillToggle,onClear:e.onAgentSkillsClear,onDisableAll:e.onAgentSkillsDisableAll,onConfigReload:e.onConfigReload,onConfigSave:e.onConfigSave}):m}
              ${e.activePanel==="channels"?Yp({agent:s,defaultId:n,configForm:e.configForm,agentFilesList:e.agentFilesList,agentIdentity:e.agentIdentityById[s.id]??null,snapshot:e.channelsSnapshot,loading:e.channelsLoading,error:e.channelsError,lastSuccess:e.channelsLastSuccess,onRefresh:e.onChannelsRefresh}):m}
              ${e.activePanel==="cron"?Qp({agent:s,defaultId:n,configForm:e.configForm,agentFilesList:e.agentFilesList,agentIdentity:e.agentIdentityById[s.id]??null,jobs:e.cronJobs,status:e.cronStatus,loading:e.cronLoading,error:e.cronError,onRefresh:e.onCronRefresh}):m}
            `:r`
                <div class="card">
                  <div class="card-title">Select an agent</div>
                  <div class="card-sub">Pick an agent to inspect its workspace and tools.</div>
                </div>
              `}
      </section>
    </div>
  `}function Bp(e,t,n){const i=nr(e.id,t),s=Wi(e),a=e.identity?.theme?.trim()||"Agent workspace and routing.",o=jn(e,n);return r`
    <section class="card agent-header">
      <div class="agent-header-main">
        <div class="agent-avatar agent-avatar--lg">
          ${o||s.slice(0,1)}
        </div>
        <div>
          <div class="card-title">${s}</div>
          <div class="card-sub">${a}</div>
        </div>
      </div>
      <div class="agent-header-meta">
        <div class="mono">${e.id}</div>
        ${i?r`<span class="agent-pill">${i}</span>`:m}
      </div>
    </section>
  `}function Up(e,t){return r`
    <div class="agent-tabs">
      ${[{id:"overview",label:"Overview"},{id:"files",label:"Files"},{id:"tools",label:"Tools"},{id:"skills",label:"Skills"},{id:"channels",label:"Channels"},{id:"cron",label:"Cron Jobs"}].map(i=>r`
          <button
            class="agent-tab ${e===i.id?"active":""}"
            type="button"
            @click=${()=>t(i.id)}
          >
            ${i.label}
          </button>
        `)}
    </div>
  `}function Kp(e){const{agent:t,configForm:n,agentFilesList:i,agentIdentity:s,agentIdentityLoading:a,agentIdentityError:o,configLoading:l,configSaving:d,configDirty:h,onConfigReload:p,onConfigSave:u,onModelChange:y,onModelFallbacksChange:v}=e,$=Gn(n,t.id),w=(i&&i.agentId===t.id?i.workspace:null)||$.entry?.workspace||$.defaults?.workspace||"default",_=$.entry?.model?Pt($.entry?.model):Pt($.defaults?.model),C=Pt($.defaults?.model),L=no($.entry?.model)||(_!=="-"?to(_):null),x=no($.defaults?.model)||(C!=="-"?to(C):null),T=L??x??null,I=Rp($.entry?.model),N=I?I.join(", "):"",fe=s?.name?.trim()||t.identity?.name?.trim()||t.name?.trim()||$.entry?.name||"-",Z=jn(t,s)||"-",B=Array.isArray($.entry?.skills)?$.entry?.skills:null,Ue=B?.length??null,le=a?"Loading…":o?"Unavailable":"",Me=!!(e.defaultId&&t.id===e.defaultId);return r`
    <section class="card">
      <div class="card-title">Overview</div>
      <div class="card-sub">Workspace paths and identity metadata.</div>
      <div class="agents-overview-grid" style="margin-top: 16px;">
        <div class="agent-kv">
          <div class="label">Workspace</div>
          <div class="mono">${w}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Primary Model</div>
          <div class="mono">${_}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Identity Name</div>
          <div>${fe}</div>
          ${le?r`<div class="agent-kv-sub muted">${le}</div>`:m}
        </div>
        <div class="agent-kv">
          <div class="label">Default</div>
          <div>${Me?"yes":"no"}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Identity Emoji</div>
          <div>${Z}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Skills Filter</div>
          <div>${B?`${Ue} selected`:"all skills"}</div>
        </div>
      </div>

      <div class="agent-model-select" style="margin-top: 20px;">
        <div class="label">Model Selection</div>
        <div class="row" style="gap: 12px; flex-wrap: wrap;">
          <label class="field" style="min-width: 260px; flex: 1;">
            <span>Primary model${Me?" (default)":""}</span>
            <select
              .value=${T??""}
              ?disabled=${!n||l||d}
              @change=${be=>y(t.id,be.target.value||null)}
            >
              ${Me?m:r`
                      <option value="">
                        ${x?`Inherit default (${x})`:"Inherit default"}
                      </option>
                    `}
              ${Fp(n,T??void 0)}
            </select>
          </label>
          <label class="field" style="min-width: 260px; flex: 1;">
            <span>Fallbacks (comma-separated)</span>
            <input
              .value=${N}
              ?disabled=${!n||l||d}
              placeholder="provider/model, provider/model"
              @input=${be=>v(t.id,Mp(be.target.value))}
            />
          </label>
        </div>
        <div class="row" style="justify-content: flex-end; gap: 8px;">
          <button
            class="btn btn--sm"
            ?disabled=${l}
            @click=${p}
          >
            Reload Config
          </button>
          <button
            class="btn btn--sm primary"
            ?disabled=${d||!h}
            @click=${u}
          >
            ${d?"Saving…":"Save"}
          </button>
        </div>
      </div>
    </section>
  `}function sr(e,t){return r`
    <section class="card">
      <div class="card-title">Agent Context</div>
      <div class="card-sub">${t}</div>
      <div class="agents-overview-grid" style="margin-top: 16px;">
        <div class="agent-kv">
          <div class="label">Workspace</div>
          <div class="mono">${e.workspace}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Primary Model</div>
          <div class="mono">${e.model}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Identity Name</div>
          <div>${e.identityName}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Identity Emoji</div>
          <div>${e.identityEmoji}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Skills Filter</div>
          <div>${e.skillsLabel}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Default</div>
          <div>${e.isDefault?"yes":"no"}</div>
        </div>
      </div>
    </section>
  `}function zp(e,t){const n=e.channelMeta?.find(i=>i.id===t);return n?.label?n.label:e.channelLabels?.[t]??t}function Hp(e){if(!e)return[];const t=new Set;for(const s of e.channelOrder??[])t.add(s);for(const s of e.channelMeta??[])t.add(s.id);for(const s of Object.keys(e.channelAccounts??{}))t.add(s);const n=[],i=e.channelOrder?.length?e.channelOrder:Array.from(t);for(const s of i)t.has(s)&&(n.push(s),t.delete(s));for(const s of t)n.push(s);return n.map(s=>({id:s,label:zp(e,s),accounts:e.channelAccounts?.[s]??[]}))}const jp=["groupPolicy","streamMode","dmPolicy"];function Gp(e,t){if(!e)return null;const i=(e.channels??{})[t];if(i&&typeof i=="object")return i;const s=e[t];return s&&typeof s=="object"?s:null}function Wp(e){if(e==null)return"n/a";if(typeof e=="string"||typeof e=="number"||typeof e=="boolean")return String(e);try{return JSON.stringify(e)}catch{return"n/a"}}function qp(e,t){const n=Gp(e,t);return n?jp.flatMap(i=>i in n?[{label:i,value:Wp(n[i])}]:[]):[]}function Vp(e){let t=0,n=0,i=0;for(const s of e){const a=s.probe&&typeof s.probe=="object"&&"ok"in s.probe?!!s.probe.ok:!1;(s.connected===!0||s.running===!0||a)&&(t+=1),s.configured&&(n+=1),s.enabled&&(i+=1)}return{total:e.length,connected:t,configured:n,enabled:i}}function Yp(e){const t=ir(e.agent,e.configForm,e.agentFilesList,e.defaultId,e.agentIdentity),n=Hp(e.snapshot),i=e.lastSuccess?U(e.lastSuccess):"never";return r`
    <section class="grid grid-cols-2">
      ${sr(t,"Workspace, identity, and model configuration.")}
      <section class="card">
        <div class="row" style="justify-content: space-between;">
          <div>
            <div class="card-title">Channels</div>
            <div class="card-sub">Gateway-wide channel status snapshot.</div>
          </div>
          <button class="btn btn--sm" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Refreshing…":"Refresh"}
          </button>
        </div>
        <div class="muted" style="margin-top: 8px;">
          Last refresh: ${i}
        </div>
        ${e.error?r`<div class="callout danger" style="margin-top: 12px;">${e.error}</div>`:m}
        ${e.snapshot?m:r`
                <div class="callout info" style="margin-top: 12px">Load channels to see live status.</div>
              `}
        ${n.length===0?r`
                <div class="muted" style="margin-top: 16px">No channels found.</div>
              `:r`
              <div class="list" style="margin-top: 16px;">
                ${n.map(s=>{const a=Vp(s.accounts),o=a.total?`${a.connected}/${a.total} connected`:"no accounts",l=a.configured?`${a.configured} configured`:"not configured",d=a.total?`${a.enabled} enabled`:"disabled",h=qp(e.configForm,s.id);return r`
                    <div class="list-item">
                      <div class="list-main">
                        <div class="list-title">${s.label}</div>
                        <div class="list-sub mono">${s.id}</div>
                      </div>
                      <div class="list-meta">
                        <div>${o}</div>
                        <div>${l}</div>
                        <div>${d}</div>
                        ${h.length>0?h.map(p=>r`<div>${p.label}: ${p.value}</div>`):m}
                      </div>
                    </div>
                  `})}
              </div>
            `}
      </section>
    </section>
  `}function Qp(e){const t=ir(e.agent,e.configForm,e.agentFilesList,e.defaultId,e.agentIdentity),n=e.jobs.filter(i=>i.agentId===e.agent.id);return r`
    <section class="grid grid-cols-2">
      ${sr(t,"Workspace and scheduling targets.")}
      <section class="card">
        <div class="row" style="justify-content: space-between;">
          <div>
            <div class="card-title">Scheduler</div>
            <div class="card-sub">Gateway cron status.</div>
          </div>
          <button class="btn btn--sm" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Refreshing…":"Refresh"}
          </button>
        </div>
        <div class="stat-grid" style="margin-top: 16px;">
          <div class="stat">
            <div class="stat-label">Enabled</div>
            <div class="stat-value">
              ${e.status?e.status.enabled?"Yes":"No":"n/a"}
            </div>
          </div>
          <div class="stat">
            <div class="stat-label">Jobs</div>
            <div class="stat-value">${e.status?.jobs??"n/a"}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Next wake</div>
            <div class="stat-value">${Ps(e.status?.nextWakeAtMs??null)}</div>
          </div>
        </div>
        ${e.error?r`<div class="callout danger" style="margin-top: 12px;">${e.error}</div>`:m}
      </section>
    </section>
    <section class="card">
      <div class="card-title">Agent Cron Jobs</div>
      <div class="card-sub">Scheduled jobs targeting this agent.</div>
      ${n.length===0?r`
              <div class="muted" style="margin-top: 16px">No jobs assigned.</div>
            `:r`
              <div class="list" style="margin-top: 16px;">
                ${n.map(i=>r`
                  <div class="list-item">
                    <div class="list-main">
                      <div class="list-title">${i.name}</div>
                      ${i.description?r`<div class="list-sub">${i.description}</div>`:m}
                      <div class="chip-row" style="margin-top: 6px;">
                        <span class="chip">${er(i)}</span>
                        <span class="chip ${i.enabled?"chip-ok":"chip-warn"}">
                          ${i.enabled?"enabled":"disabled"}
                        </span>
                        <span class="chip">${i.sessionTarget}</span>
                      </div>
                    </div>
                    <div class="list-meta">
                      <div class="mono">${Xl(i)}</div>
                      <div class="muted">${tr(i)}</div>
                    </div>
                  </div>
                `)}
              </div>
            `}
    </section>
  `}function Jp(e){const t=e.agentFilesList?.agentId===e.agentId?e.agentFilesList:null,n=t?.files??[],i=e.agentFileActive??null,s=i?n.find(d=>d.name===i)??null:null,a=i?e.agentFileContents[i]??"":"",o=i?e.agentFileDrafts[i]??a:"",l=i?o!==a:!1;return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Core Files</div>
          <div class="card-sub">Bootstrap persona, identity, and tool guidance.</div>
        </div>
        <button
          class="btn btn--sm"
          ?disabled=${e.agentFilesLoading}
          @click=${()=>e.onLoadFiles(e.agentId)}
        >
          ${e.agentFilesLoading?"Loading…":"Refresh"}
        </button>
      </div>
      ${t?r`<div class="muted mono" style="margin-top: 8px;">Workspace: ${t.workspace}</div>`:m}
      ${e.agentFilesError?r`<div class="callout danger" style="margin-top: 12px;">${e.agentFilesError}</div>`:m}
      ${t?r`
              <div class="agent-files-grid" style="margin-top: 16px;">
                <div class="agent-files-list">
                  ${n.length===0?r`
                          <div class="muted">No files found.</div>
                        `:n.map(d=>Zp(d,i,()=>e.onSelectFile(d.name)))}
                </div>
                <div class="agent-files-editor">
                  ${s?r`
                          <div class="agent-file-header">
                            <div>
                              <div class="agent-file-title mono">${s.name}</div>
                              <div class="agent-file-sub mono">${s.path}</div>
                            </div>
                            <div class="agent-file-actions">
                              <button
                                class="btn btn--sm"
                                ?disabled=${!l}
                                @click=${()=>e.onFileReset(s.name)}
                              >
                                Reset
                              </button>
                              <button
                                class="btn btn--sm primary"
                                ?disabled=${e.agentFileSaving||!l}
                                @click=${()=>e.onFileSave(s.name)}
                              >
                                ${e.agentFileSaving?"Saving…":"Save"}
                              </button>
                            </div>
                          </div>
                          ${s.missing?r`
                                  <div class="callout info" style="margin-top: 10px">
                                    This file is missing. Saving will create it in the agent workspace.
                                  </div>
                                `:m}
                          <label class="field" style="margin-top: 12px;">
                            <span>Content</span>
                            <textarea
                              .value=${o}
                              @input=${d=>e.onFileDraftChange(s.name,d.target.value)}
                            ></textarea>
                          </label>
                        `:r`
                          <div class="muted">Select a file to edit.</div>
                        `}
                </div>
              </div>
            `:r`
              <div class="callout info" style="margin-top: 12px">
                Load the agent workspace files to edit core instructions.
              </div>
            `}
    </section>
  `}function Zp(e,t,n){const i=e.missing?"Missing":`${Ip(e.size)} · ${U(e.updatedAtMs??null)}`;return r`
    <button
      type="button"
      class="agent-file-row ${t===e.name?"active":""}"
      @click=${n}
    >
      <div>
        <div class="agent-file-name mono">${e.name}</div>
        <div class="agent-file-meta">${i}</div>
      </div>
      ${e.missing?r`
              <span class="agent-pill warn">missing</span>
            `:m}
    </button>
  `}function Xp(e){const t=Gn(e.configForm,e.agentId),n=t.entry?.tools??{},i=t.globalTools??{},s=n.profile??i.profile??"full",a=n.profile?"agent override":i.profile?"global default":"default",o=Array.isArray(n.allow)&&n.allow.length>0,l=Array.isArray(i.allow)&&i.allow.length>0,d=!!e.configForm&&!e.configLoading&&!e.configSaving&&!o,h=o?[]:Array.isArray(n.alsoAllow)?n.alsoAllow:[],p=o?[]:Array.isArray(n.deny)?n.deny:[],u=o?{allow:n.allow??[],deny:n.deny??[]}:xp(s)??void 0,y=eo.flatMap(_=>_.tools.map(C=>C.id)),v=_=>{const C=Op(_,u),L=io(_,h),x=io(_,p);return{allowed:(C||L)&&!x,baseAllowed:C,denied:x}},$=y.filter(_=>v(_).allowed).length,g=(_,C)=>{const L=new Set(h.map(N=>Ae(N)).filter(N=>N.length>0)),x=new Set(p.map(N=>Ae(N)).filter(N=>N.length>0)),T=v(_).baseAllowed,I=Ae(_);C?(x.delete(I),T||L.add(I)):(L.delete(I),x.add(I)),e.onOverridesChange(e.agentId,[...L],[...x])},w=_=>{const C=new Set(h.map(x=>Ae(x)).filter(x=>x.length>0)),L=new Set(p.map(x=>Ae(x)).filter(x=>x.length>0));for(const x of y){const T=v(x).baseAllowed,I=Ae(x);_?(L.delete(I),T||C.add(I)):(C.delete(I),L.add(I))}e.onOverridesChange(e.agentId,[...C],[...L])};return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Tool Access</div>
          <div class="card-sub">
            Profile + per-tool overrides for this agent.
            <span class="mono">${$}/${y.length}</span> enabled.
          </div>
        </div>
        <div class="row" style="gap: 8px;">
          <button
            class="btn btn--sm"
            ?disabled=${!d}
            @click=${()=>w(!0)}
          >
            Enable All
          </button>
          <button
            class="btn btn--sm"
            ?disabled=${!d}
            @click=${()=>w(!1)}
          >
            Disable All
          </button>
          <button
            class="btn btn--sm"
            ?disabled=${e.configLoading}
            @click=${e.onConfigReload}
          >
            Reload Config
          </button>
          <button
            class="btn btn--sm primary"
            ?disabled=${e.configSaving||!e.configDirty}
            @click=${e.onConfigSave}
          >
            ${e.configSaving?"Saving…":"Save"}
          </button>
        </div>
      </div>

      ${e.configForm?m:r`
              <div class="callout info" style="margin-top: 12px">
                Load the gateway config to adjust tool profiles.
              </div>
            `}
      ${o?r`
              <div class="callout info" style="margin-top: 12px">
                This agent is using an explicit allowlist in config. Tool overrides are managed in the Config tab.
              </div>
            `:m}
      ${l?r`
              <div class="callout info" style="margin-top: 12px">
                Global tools.allow is set. Agent overrides cannot enable tools that are globally blocked.
              </div>
            `:m}

      <div class="agent-tools-meta" style="margin-top: 16px;">
        <div class="agent-kv">
          <div class="label">Profile</div>
          <div class="mono">${s}</div>
        </div>
        <div class="agent-kv">
          <div class="label">Source</div>
          <div>${a}</div>
        </div>
        ${e.configDirty?r`
                <div class="agent-kv">
                  <div class="label">Status</div>
                  <div class="mono">unsaved</div>
                </div>
              `:m}
      </div>

      <div class="agent-tools-presets" style="margin-top: 16px;">
        <div class="label">Quick Presets</div>
        <div class="agent-tools-buttons">
          ${Lp.map(_=>r`
              <button
                class="btn btn--sm ${s===_.id?"active":""}"
                ?disabled=${!d}
                @click=${()=>e.onProfileChange(e.agentId,_.id,!0)}
              >
                ${_.label}
              </button>
            `)}
          <button
            class="btn btn--sm"
            ?disabled=${!d}
            @click=${()=>e.onProfileChange(e.agentId,null,!1)}
          >
            Inherit
          </button>
        </div>
      </div>

      <div class="agent-tools-grid" style="margin-top: 20px;">
        ${eo.map(_=>r`
            <div class="agent-tools-section">
              <div class="agent-tools-header">${_.label}</div>
              <div class="agent-tools-list">
                ${_.tools.map(C=>{const{allowed:L}=v(C.id);return r`
                    <div class="agent-tool-row">
                      <div>
                        <div class="agent-tool-title mono">${C.label}</div>
                        <div class="agent-tool-sub">${C.description}</div>
                      </div>
                      <label class="cfg-toggle">
                        <input
                          type="checkbox"
                          .checked=${L}
                          ?disabled=${!d}
                          @change=${x=>g(C.id,x.target.checked)}
                        />
                        <span class="cfg-toggle__track"></span>
                      </label>
                    </div>
                  `})}
              </div>
            </div>
          `)}
      </div>
    </section>
  `}const fn=[{id:"workspace",label:"Workspace Skills",sources:["openclaw-workspace"]},{id:"built-in",label:"Built-in Skills",sources:["openclaw-bundled"]},{id:"installed",label:"Installed Skills",sources:["openclaw-managed"]},{id:"extra",label:"Extra Skills",sources:["openclaw-extra"]}];function ev(e){const t=new Map;for(const a of fn)t.set(a.id,{id:a.id,label:a.label,skills:[]});const n=fn.find(a=>a.id==="built-in"),i={id:"other",label:"Other Skills",skills:[]};for(const a of e){const o=a.bundled?n:fn.find(l=>l.sources.includes(a.source));o?t.get(o.id)?.skills.push(a):i.skills.push(a)}const s=fn.map(a=>t.get(a.id)).filter(a=>!!(a&&a.skills.length>0));return i.skills.length>0&&s.push(i),s}function tv(e){const t=!!e.configForm&&!e.configLoading&&!e.configSaving,n=Gn(e.configForm,e.agentId),i=Array.isArray(n.entry?.skills)?n.entry?.skills:void 0,s=new Set((i??[]).map(v=>v.trim()).filter(Boolean)),a=i!==void 0,o=!!(e.report&&e.activeAgentId===e.agentId),l=o?e.report?.skills??[]:[],d=e.filter.trim().toLowerCase(),h=d?l.filter(v=>[v.name,v.description,v.source].join(" ").toLowerCase().includes(d)):l,p=ev(h),u=a?l.filter(v=>s.has(v.name)).length:l.length,y=l.length;return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Skills</div>
          <div class="card-sub">
            Per-agent skill allowlist and workspace skills.
            ${y>0?r`<span class="mono">${u}/${y}</span>`:m}
          </div>
        </div>
        <div class="row" style="gap: 8px;">
          <button class="btn btn--sm" ?disabled=${!t} @click=${()=>e.onClear(e.agentId)}>
            Use All
          </button>
          <button class="btn btn--sm" ?disabled=${!t} @click=${()=>e.onDisableAll(e.agentId)}>
            Disable All
          </button>
          <button
            class="btn btn--sm"
            ?disabled=${e.configLoading}
            @click=${e.onConfigReload}
          >
            Reload Config
          </button>
          <button class="btn btn--sm" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Loading…":"Refresh"}
          </button>
          <button
            class="btn btn--sm primary"
            ?disabled=${e.configSaving||!e.configDirty}
            @click=${e.onConfigSave}
          >
            ${e.configSaving?"Saving…":"Save"}
          </button>
        </div>
      </div>

      ${e.configForm?m:r`
              <div class="callout info" style="margin-top: 12px">
                Load the gateway config to set per-agent skills.
              </div>
            `}
      ${a?r`
              <div class="callout info" style="margin-top: 12px">This agent uses a custom skill allowlist.</div>
            `:r`
              <div class="callout info" style="margin-top: 12px">
                All skills are enabled. Disabling any skill will create a per-agent allowlist.
              </div>
            `}
      ${!o&&!e.loading?r`
              <div class="callout info" style="margin-top: 12px">
                Load skills for this agent to view workspace-specific entries.
              </div>
            `:m}
      ${e.error?r`<div class="callout danger" style="margin-top: 12px;">${e.error}</div>`:m}

      <div class="filters" style="margin-top: 14px;">
        <label class="field" style="flex: 1;">
          <span>Filter</span>
          <input
            .value=${e.filter}
            @input=${v=>e.onFilterChange(v.target.value)}
            placeholder="Search skills"
          />
        </label>
        <div class="muted">${h.length} shown</div>
      </div>

      ${h.length===0?r`
              <div class="muted" style="margin-top: 16px">No skills found.</div>
            `:r`
              <div class="agent-skills-groups" style="margin-top: 16px;">
                ${p.map(v=>nv(v,{agentId:e.agentId,allowSet:s,usingAllowlist:a,editable:t,onToggle:e.onToggle}))}
              </div>
            `}
    </section>
  `}function nv(e,t){const n=e.id==="workspace"||e.id==="built-in";return r`
    <details class="agent-skills-group" ?open=${!n}>
      <summary class="agent-skills-header">
        <span>${e.label}</span>
        <span class="muted">${e.skills.length}</span>
      </summary>
      <div class="list skills-grid">
        ${e.skills.map(i=>iv(i,{agentId:t.agentId,allowSet:t.allowSet,usingAllowlist:t.usingAllowlist,editable:t.editable,onToggle:t.onToggle}))}
      </div>
    </details>
  `}function iv(e,t){const n=t.usingAllowlist?t.allowSet.has(e.name):!0,i=[...e.missing.bins.map(a=>`bin:${a}`),...e.missing.env.map(a=>`env:${a}`),...e.missing.config.map(a=>`config:${a}`),...e.missing.os.map(a=>`os:${a}`)],s=[];return e.disabled&&s.push("disabled"),e.blockedByAllowlist&&s.push("blocked by allowlist"),r`
    <div class="list-item agent-skill-row">
      <div class="list-main">
        <div class="list-title">
          ${e.emoji?`${e.emoji} `:""}${e.name}
        </div>
        <div class="list-sub">${e.description}</div>
        <div class="chip-row" style="margin-top: 6px;">
          <span class="chip">${e.source}</span>
          <span class="chip ${e.eligible?"chip-ok":"chip-warn"}">
            ${e.eligible?"eligible":"blocked"}
          </span>
          ${e.disabled?r`
                  <span class="chip chip-warn">disabled</span>
                `:m}
        </div>
        ${i.length>0?r`<div class="muted" style="margin-top: 6px;">Missing: ${i.join(", ")}</div>`:m}
        ${s.length>0?r`<div class="muted" style="margin-top: 6px;">Reason: ${s.join(", ")}</div>`:m}
      </div>
      <div class="list-meta">
        <label class="cfg-toggle">
          <input
            type="checkbox"
            .checked=${n}
            ?disabled=${!t.editable}
            @change=${a=>t.onToggle(t.agentId,e.name,a.target.checked)}
          />
          <span class="cfg-toggle__track"></span>
        </label>
      </div>
    </div>
  `}function Se(e){if(e)return Array.isArray(e.type)?e.type.filter(n=>n!=="null")[0]??e.type[0]:e.type}function ar(e){if(!e)return"";if(e.default!==void 0)return e.default;switch(Se(e)){case"object":return{};case"array":return[];case"boolean":return!1;case"number":case"integer":return 0;case"string":return"";default:return""}}function Wn(e){return e.filter(t=>typeof t=="string").join(".")}function de(e,t){const n=Wn(e),i=t[n];if(i)return i;const s=n.split(".");for(const[a,o]of Object.entries(t)){if(!a.includes("*"))continue;const l=a.split(".");if(l.length!==s.length)continue;let d=!0;for(let h=0;h<s.length;h+=1)if(l[h]!=="*"&&l[h]!==s[h]){d=!1;break}if(d)return o}}function Ie(e){return e.replace(/_/g," ").replace(/([a-z0-9])([A-Z])/g,"$1 $2").replace(/\s+/g," ").replace(/^./,t=>t.toUpperCase())}function sv(e){const t=Wn(e).toLowerCase();return t.includes("token")||t.includes("password")||t.includes("secret")||t.includes("apikey")||t.endsWith("key")}const av=new Set(["title","description","default","nullable"]);function ov(e){return Object.keys(e??{}).filter(n=>!av.has(n)).length===0}function lv(e){if(e===void 0)return"";try{return JSON.stringify(e,null,2)??""}catch{return""}}const Gt={chevronDown:r`
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <polyline points="6 9 12 15 18 9"></polyline>
    </svg>
  `,plus:r`
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <line x1="12" y1="5" x2="12" y2="19"></line>
      <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
  `,minus:r`
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <line x1="5" y1="12" x2="19" y2="12"></line>
    </svg>
  `,trash:r`
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <polyline points="3 6 5 6 21 6"></polyline>
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
    </svg>
  `,edit:r`
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
    </svg>
  `};function Le(e){const{schema:t,value:n,path:i,hints:s,unsupported:a,disabled:o,onPatch:l}=e,d=e.showLabel??!0,h=Se(t),p=de(i,s),u=p?.label??t.title??Ie(String(i.at(-1))),y=p?.help??t.description,v=Wn(i);if(a.has(v))return r`<div class="cfg-field cfg-field--error">
      <div class="cfg-field__label">${u}</div>
      <div class="cfg-field__error">Unsupported schema node. Use Raw mode.</div>
    </div>`;if(t.anyOf||t.oneOf){const g=(t.anyOf??t.oneOf??[]).filter(T=>!(T.type==="null"||Array.isArray(T.type)&&T.type.includes("null")));if(g.length===1)return Le({...e,schema:g[0]});const w=T=>{if(T.const!==void 0)return T.const;if(T.enum&&T.enum.length===1)return T.enum[0]},_=g.map(w),C=_.every(T=>T!==void 0);if(C&&_.length>0&&_.length<=5){const T=n??t.default;return r`
        <div class="cfg-field">
          ${d?r`<label class="cfg-field__label">${u}</label>`:m}
          ${y?r`<div class="cfg-field__help">${y}</div>`:m}
          <div class="cfg-segmented">
            ${_.map(I=>r`
              <button
                type="button"
                class="cfg-segmented__btn ${I===T||String(I)===String(T)?"active":""}"
                ?disabled=${o}
                @click=${()=>l(i,I)}
              >
                ${String(I)}
              </button>
            `)}
          </div>
        </div>
      `}if(C&&_.length>5)return ao({...e,options:_,value:n??t.default});const L=new Set(g.map(T=>Se(T)).filter(Boolean)),x=new Set([...L].map(T=>T==="integer"?"number":T));if([...x].every(T=>["string","number","boolean"].includes(T))){const T=x.has("string"),I=x.has("number");if(x.has("boolean")&&x.size===1)return Le({...e,schema:{...t,type:"boolean",anyOf:void 0,oneOf:void 0}});if(T||I)return so({...e,inputType:I&&!T?"number":"text"})}}if(t.enum){const $=t.enum;if($.length<=5){const g=n??t.default;return r`
        <div class="cfg-field">
          ${d?r`<label class="cfg-field__label">${u}</label>`:m}
          ${y?r`<div class="cfg-field__help">${y}</div>`:m}
          <div class="cfg-segmented">
            ${$.map(w=>r`
              <button
                type="button"
                class="cfg-segmented__btn ${w===g||String(w)===String(g)?"active":""}"
                ?disabled=${o}
                @click=${()=>l(i,w)}
              >
                ${String(w)}
              </button>
            `)}
          </div>
        </div>
      `}return ao({...e,options:$,value:n??t.default})}if(h==="object")return cv(e);if(h==="array")return dv(e);if(h==="boolean"){const $=typeof n=="boolean"?n:typeof t.default=="boolean"?t.default:!1;return r`
      <label class="cfg-toggle-row ${o?"disabled":""}">
        <div class="cfg-toggle-row__content">
          <span class="cfg-toggle-row__label">${u}</span>
          ${y?r`<span class="cfg-toggle-row__help">${y}</span>`:m}
        </div>
        <div class="cfg-toggle">
          <input
            type="checkbox"
            .checked=${$}
            ?disabled=${o}
            @change=${g=>l(i,g.target.checked)}
          />
          <span class="cfg-toggle__track"></span>
        </div>
      </label>
    `}return h==="number"||h==="integer"?rv(e):h==="string"?so({...e,inputType:"text"}):r`
    <div class="cfg-field cfg-field--error">
      <div class="cfg-field__label">${u}</div>
      <div class="cfg-field__error">Unsupported type: ${h}. Use Raw mode.</div>
    </div>
  `}function so(e){const{schema:t,value:n,path:i,hints:s,disabled:a,onPatch:o,inputType:l}=e,d=e.showLabel??!0,h=de(i,s),p=h?.label??t.title??Ie(String(i.at(-1))),u=h?.help??t.description,y=h?.sensitive??sv(i),v=h?.placeholder??(y?"••••":t.default!==void 0?`Default: ${String(t.default)}`:""),$=n??"";return r`
    <div class="cfg-field">
      ${d?r`<label class="cfg-field__label">${p}</label>`:m}
      ${u?r`<div class="cfg-field__help">${u}</div>`:m}
      <div class="cfg-input-wrap">
        <input
          type=${y?"password":l}
          class="cfg-input"
          placeholder=${v}
          .value=${$==null?"":String($)}
          ?disabled=${a}
          @input=${g=>{const w=g.target.value;if(l==="number"){if(w.trim()===""){o(i,void 0);return}const _=Number(w);o(i,Number.isNaN(_)?w:_);return}o(i,w)}}
          @change=${g=>{if(l==="number")return;const w=g.target.value;o(i,w.trim())}}
        />
        ${t.default!==void 0?r`
          <button
            type="button"
            class="cfg-input__reset"
            title="Reset to default"
            ?disabled=${a}
            @click=${()=>o(i,t.default)}
          >↺</button>
        `:m}
      </div>
    </div>
  `}function rv(e){const{schema:t,value:n,path:i,hints:s,disabled:a,onPatch:o}=e,l=e.showLabel??!0,d=de(i,s),h=d?.label??t.title??Ie(String(i.at(-1))),p=d?.help??t.description,u=n??t.default??"",y=typeof u=="number"?u:0;return r`
    <div class="cfg-field">
      ${l?r`<label class="cfg-field__label">${h}</label>`:m}
      ${p?r`<div class="cfg-field__help">${p}</div>`:m}
      <div class="cfg-number">
        <button
          type="button"
          class="cfg-number__btn"
          ?disabled=${a}
          @click=${()=>o(i,y-1)}
        >−</button>
        <input
          type="number"
          class="cfg-number__input"
          .value=${u==null?"":String(u)}
          ?disabled=${a}
          @input=${v=>{const $=v.target.value,g=$===""?void 0:Number($);o(i,g)}}
        />
        <button
          type="button"
          class="cfg-number__btn"
          ?disabled=${a}
          @click=${()=>o(i,y+1)}
        >+</button>
      </div>
    </div>
  `}function ao(e){const{schema:t,value:n,path:i,hints:s,disabled:a,options:o,onPatch:l}=e,d=e.showLabel??!0,h=de(i,s),p=h?.label??t.title??Ie(String(i.at(-1))),u=h?.help??t.description,y=n??t.default,v=o.findIndex(g=>g===y||String(g)===String(y)),$="__unset__";return r`
    <div class="cfg-field">
      ${d?r`<label class="cfg-field__label">${p}</label>`:m}
      ${u?r`<div class="cfg-field__help">${u}</div>`:m}
      <select
        class="cfg-select"
        ?disabled=${a}
        .value=${v>=0?String(v):$}
        @change=${g=>{const w=g.target.value;l(i,w===$?void 0:o[Number(w)])}}
      >
        <option value=${$}>Select...</option>
        ${o.map((g,w)=>r`
          <option value=${String(w)}>${String(g)}</option>
        `)}
      </select>
    </div>
  `}function cv(e){const{schema:t,value:n,path:i,hints:s,unsupported:a,disabled:o,onPatch:l}=e,d=de(i,s),h=d?.label??t.title??Ie(String(i.at(-1))),p=d?.help??t.description,u=n??t.default,y=u&&typeof u=="object"&&!Array.isArray(u)?u:{},v=t.properties??{},g=Object.entries(v).toSorted((L,x)=>{const T=de([...i,L[0]],s)?.order??0,I=de([...i,x[0]],s)?.order??0;return T!==I?T-I:L[0].localeCompare(x[0])}),w=new Set(Object.keys(v)),_=t.additionalProperties,C=!!_&&typeof _=="object";return i.length===1?r`
      <div class="cfg-fields">
        ${g.map(([L,x])=>Le({schema:x,value:y[L],path:[...i,L],hints:s,unsupported:a,disabled:o,onPatch:l}))}
        ${C?oo({schema:_,value:y,path:i,hints:s,unsupported:a,disabled:o,reservedKeys:w,onPatch:l}):m}
      </div>
    `:r`
    <details class="cfg-object" open>
      <summary class="cfg-object__header">
        <span class="cfg-object__title">${h}</span>
        <span class="cfg-object__chevron">${Gt.chevronDown}</span>
      </summary>
      ${p?r`<div class="cfg-object__help">${p}</div>`:m}
      <div class="cfg-object__content">
        ${g.map(([L,x])=>Le({schema:x,value:y[L],path:[...i,L],hints:s,unsupported:a,disabled:o,onPatch:l}))}
        ${C?oo({schema:_,value:y,path:i,hints:s,unsupported:a,disabled:o,reservedKeys:w,onPatch:l}):m}
      </div>
    </details>
  `}function dv(e){const{schema:t,value:n,path:i,hints:s,unsupported:a,disabled:o,onPatch:l}=e,d=e.showLabel??!0,h=de(i,s),p=h?.label??t.title??Ie(String(i.at(-1))),u=h?.help??t.description,y=Array.isArray(t.items)?t.items[0]:t.items;if(!y)return r`
      <div class="cfg-field cfg-field--error">
        <div class="cfg-field__label">${p}</div>
        <div class="cfg-field__error">Unsupported array schema. Use Raw mode.</div>
      </div>
    `;const v=Array.isArray(n)?n:Array.isArray(t.default)?t.default:[];return r`
    <div class="cfg-array">
      <div class="cfg-array__header">
        ${d?r`<span class="cfg-array__label">${p}</span>`:m}
        <span class="cfg-array__count">${v.length} item${v.length!==1?"s":""}</span>
        <button
          type="button"
          class="cfg-array__add"
          ?disabled=${o}
          @click=${()=>{const $=[...v,ar(y)];l(i,$)}}
        >
          <span class="cfg-array__add-icon">${Gt.plus}</span>
          Add
        </button>
      </div>
      ${u?r`<div class="cfg-array__help">${u}</div>`:m}

      ${v.length===0?r`
              <div class="cfg-array__empty">No items yet. Click "Add" to create one.</div>
            `:r`
        <div class="cfg-array__items">
          ${v.map(($,g)=>r`
            <div class="cfg-array__item">
              <div class="cfg-array__item-header">
                <span class="cfg-array__item-index">#${g+1}</span>
                <button
                  type="button"
                  class="cfg-array__item-remove"
                  title="Remove item"
                  ?disabled=${o}
                  @click=${()=>{const w=[...v];w.splice(g,1),l(i,w)}}
                >
                  ${Gt.trash}
                </button>
              </div>
              <div class="cfg-array__item-content">
                ${Le({schema:y,value:$,path:[...i,g],hints:s,unsupported:a,disabled:o,showLabel:!1,onPatch:l})}
              </div>
            </div>
          `)}
        </div>
      `}
    </div>
  `}function oo(e){const{schema:t,value:n,path:i,hints:s,unsupported:a,disabled:o,reservedKeys:l,onPatch:d}=e,h=ov(t),p=Object.entries(n??{}).filter(([u])=>!l.has(u));return r`
    <div class="cfg-map">
      <div class="cfg-map__header">
        <span class="cfg-map__label">Custom entries</span>
        <button
          type="button"
          class="cfg-map__add"
          ?disabled=${o}
          @click=${()=>{const u={...n};let y=1,v=`custom-${y}`;for(;v in u;)y+=1,v=`custom-${y}`;u[v]=h?{}:ar(t),d(i,u)}}
        >
          <span class="cfg-map__add-icon">${Gt.plus}</span>
          Add Entry
        </button>
      </div>

      ${p.length===0?r`
              <div class="cfg-map__empty">No custom entries.</div>
            `:r`
        <div class="cfg-map__items">
          ${p.map(([u,y])=>{const v=[...i,u],$=lv(y);return r`
              <div class="cfg-map__item">
                <div class="cfg-map__item-key">
                  <input
                    type="text"
                    class="cfg-input cfg-input--sm"
                    placeholder="Key"
                    .value=${u}
                    ?disabled=${o}
                    @change=${g=>{const w=g.target.value.trim();if(!w||w===u)return;const _={...n};w in _||(_[w]=_[u],delete _[u],d(i,_))}}
                  />
                </div>
                <div class="cfg-map__item-value">
                  ${h?r`
                        <textarea
                          class="cfg-textarea cfg-textarea--sm"
                          placeholder="JSON value"
                          rows="2"
                          .value=${$}
                          ?disabled=${o}
                          @change=${g=>{const w=g.target,_=w.value.trim();if(!_){d(v,void 0);return}try{d(v,JSON.parse(_))}catch{w.value=$}}}
                        ></textarea>
                      `:Le({schema:t,value:y,path:v,hints:s,unsupported:a,disabled:o,showLabel:!1,onPatch:d})}
                </div>
                <button
                  type="button"
                  class="cfg-map__item-remove"
                  title="Remove entry"
                  ?disabled=${o}
                  @click=${()=>{const g={...n};delete g[u],d(i,g)}}
                >
                  ${Gt.trash}
                </button>
              </div>
            `})}
        </div>
      `}
    </div>
  `}const lo={env:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="12" r="3"></circle>
      <path
        d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
      ></path>
    </svg>
  `,update:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
      <polyline points="7 10 12 15 17 10"></polyline>
      <line x1="12" y1="15" x2="12" y2="3"></line>
    </svg>
  `,agents:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path
        d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z"
      ></path>
      <circle cx="8" cy="14" r="1"></circle>
      <circle cx="16" cy="14" r="1"></circle>
    </svg>
  `,auth:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
    </svg>
  `,channels:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
  `,messages:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
      <polyline points="22,6 12,13 2,6"></polyline>
    </svg>
  `,commands:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <polyline points="4 17 10 11 4 5"></polyline>
      <line x1="12" y1="19" x2="20" y2="19"></line>
    </svg>
  `,hooks:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
    </svg>
  `,skills:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <polygon
        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
      ></polygon>
    </svg>
  `,tools:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path
        d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
      ></path>
    </svg>
  `,gateway:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path
        d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
      ></path>
    </svg>
  `,wizard:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M15 4V2"></path>
      <path d="M15 16v-2"></path>
      <path d="M8 9h2"></path>
      <path d="M20 9h2"></path>
      <path d="M17.8 11.8 19 13"></path>
      <path d="M15 9h0"></path>
      <path d="M17.8 6.2 19 5"></path>
      <path d="m3 21 9-9"></path>
      <path d="M12.2 6.2 11 5"></path>
    </svg>
  `,meta:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M12 20h9"></path>
      <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"></path>
    </svg>
  `,logging:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
      <line x1="16" y1="13" x2="8" y2="13"></line>
      <line x1="16" y1="17" x2="8" y2="17"></line>
      <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
  `,browser:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="12" r="10"></circle>
      <circle cx="12" cy="12" r="4"></circle>
      <line x1="21.17" y1="8" x2="12" y2="8"></line>
      <line x1="3.95" y1="6.06" x2="8.54" y2="14"></line>
      <line x1="10.88" y1="21.94" x2="15.46" y2="14"></line>
    </svg>
  `,ui:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
      <line x1="3" y1="9" x2="21" y2="9"></line>
      <line x1="9" y1="21" x2="9" y2="9"></line>
    </svg>
  `,models:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path
        d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
      ></path>
      <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
      <line x1="12" y1="22.08" x2="12" y2="12"></line>
    </svg>
  `,bindings:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
      <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
      <line x1="6" y1="6" x2="6.01" y2="6"></line>
      <line x1="6" y1="18" x2="6.01" y2="18"></line>
    </svg>
  `,broadcast:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"></path>
      <path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"></path>
      <circle cx="12" cy="12" r="2"></circle>
      <path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"></path>
      <path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"></path>
    </svg>
  `,audio:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M9 18V5l12-2v13"></path>
      <circle cx="6" cy="18" r="3"></circle>
      <circle cx="18" cy="16" r="3"></circle>
    </svg>
  `,session:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
      <circle cx="9" cy="7" r="4"></circle>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </svg>
  `,cron:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="12" r="10"></circle>
      <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
  `,web:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path
        d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
      ></path>
    </svg>
  `,discovery:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
  `,canvasHost:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
      <circle cx="8.5" cy="8.5" r="1.5"></circle>
      <polyline points="21 15 16 10 5 21"></polyline>
    </svg>
  `,talk:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
      <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
      <line x1="12" y1="19" x2="12" y2="23"></line>
      <line x1="8" y1="23" x2="16" y2="23"></line>
    </svg>
  `,plugins:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M12 2v6"></path>
      <path d="m4.93 10.93 4.24 4.24"></path>
      <path d="M2 12h6"></path>
      <path d="m4.93 13.07 4.24-4.24"></path>
      <path d="M12 22v-6"></path>
      <path d="m19.07 13.07-4.24-4.24"></path>
      <path d="M22 12h-6"></path>
      <path d="m19.07 10.93-4.24 4.24"></path>
    </svg>
  `,default:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
    </svg>
  `},Fs={env:{label:"Environment Variables",description:"Environment variables passed to the gateway process"},update:{label:"Updates",description:"Auto-update settings and release channel"},agents:{label:"Agents",description:"Agent configurations, models, and identities"},auth:{label:"Authentication",description:"API keys and authentication profiles"},channels:{label:"Channels",description:"Messaging channels (Telegram, Discord, Slack, etc.)"},messages:{label:"Messages",description:"Message handling and routing settings"},commands:{label:"Commands",description:"Custom slash commands"},hooks:{label:"Hooks",description:"Webhooks and event hooks"},skills:{label:"Skills",description:"Skill packs and capabilities"},tools:{label:"Tools",description:"Tool configurations (browser, search, etc.)"},gateway:{label:"Gateway",description:"Gateway server settings (port, auth, binding)"},wizard:{label:"Setup Wizard",description:"Setup wizard state and history"},meta:{label:"Metadata",description:"Gateway metadata and version information"},logging:{label:"Logging",description:"Log levels and output configuration"},browser:{label:"Browser",description:"Browser automation settings"},ui:{label:"UI",description:"User interface preferences"},models:{label:"Models",description:"AI model configurations and providers"},bindings:{label:"Bindings",description:"Key bindings and shortcuts"},broadcast:{label:"Broadcast",description:"Broadcast and notification settings"},audio:{label:"Audio",description:"Audio input/output settings"},session:{label:"Session",description:"Session management and persistence"},cron:{label:"Cron",description:"Scheduled tasks and automation"},web:{label:"Web",description:"Web server and API settings"},discovery:{label:"Discovery",description:"Service discovery and networking"},canvasHost:{label:"Canvas Host",description:"Canvas rendering and display"},talk:{label:"Talk",description:"Voice and speech settings"},plugins:{label:"Plugins",description:"Plugin management and extensions"}};function ro(e){return lo[e]??lo.default}function uv(e,t,n){if(!n)return!0;const i=n.toLowerCase(),s=Fs[e];return e.toLowerCase().includes(i)||s&&(s.label.toLowerCase().includes(i)||s.description.toLowerCase().includes(i))?!0:Tt(t,i)}function Tt(e,t){if(e.title?.toLowerCase().includes(t)||e.description?.toLowerCase().includes(t)||e.enum?.some(i=>String(i).toLowerCase().includes(t)))return!0;if(e.properties){for(const[i,s]of Object.entries(e.properties))if(i.toLowerCase().includes(t)||Tt(s,t))return!0}if(e.items){const i=Array.isArray(e.items)?e.items:[e.items];for(const s of i)if(s&&Tt(s,t))return!0}if(e.additionalProperties&&typeof e.additionalProperties=="object"&&Tt(e.additionalProperties,t))return!0;const n=e.anyOf??e.oneOf??e.allOf;if(n){for(const i of n)if(i&&Tt(i,t))return!0}return!1}function fv(e){if(!e.schema)return r`
      <div class="muted">Schema unavailable.</div>
    `;const t=e.schema,n=e.value??{};if(Se(t)!=="object"||!t.properties)return r`
      <div class="callout danger">Unsupported schema. Use Raw.</div>
    `;const i=new Set(e.unsupportedPaths??[]),s=t.properties,a=e.searchQuery??"",o=e.activeSection,l=e.activeSubsection??null,h=Object.entries(s).toSorted((u,y)=>{const v=de([u[0]],e.uiHints)?.order??50,$=de([y[0]],e.uiHints)?.order??50;return v!==$?v-$:u[0].localeCompare(y[0])}).filter(([u,y])=>!(o&&u!==o||a&&!uv(u,y,a)));let p=null;if(o&&l&&h.length===1){const u=h[0]?.[1];u&&Se(u)==="object"&&u.properties&&u.properties[l]&&(p={sectionKey:o,subsectionKey:l,schema:u.properties[l]})}return h.length===0?r`
      <div class="config-empty">
        <div class="config-empty__icon">${J.search}</div>
        <div class="config-empty__text">
          ${a?`No settings match "${a}"`:"No settings in this section"}
        </div>
      </div>
    `:r`
    <div class="config-form config-form--modern">
      ${p?(()=>{const{sectionKey:u,subsectionKey:y,schema:v}=p,$=de([u,y],e.uiHints),g=$?.label??v.title??Ie(y),w=$?.help??v.description??"",_=n[u],C=_&&typeof _=="object"?_[y]:void 0,L=`config-section-${u}-${y}`;return r`
              <section class="config-section-card" id=${L}>
                <div class="config-section-card__header">
                  <span class="config-section-card__icon">${ro(u)}</span>
                  <div class="config-section-card__titles">
                    <h3 class="config-section-card__title">${g}</h3>
                    ${w?r`<p class="config-section-card__desc">${w}</p>`:m}
                  </div>
                </div>
                <div class="config-section-card__content">
                  ${Le({schema:v,value:C,path:[u,y],hints:e.uiHints,unsupported:i,disabled:e.disabled??!1,showLabel:!1,onPatch:e.onPatch})}
                </div>
              </section>
            `})():h.map(([u,y])=>{const v=Fs[u]??{label:u.charAt(0).toUpperCase()+u.slice(1),description:y.description??""};return r`
              <section class="config-section-card" id="config-section-${u}">
                <div class="config-section-card__header">
                  <span class="config-section-card__icon">${ro(u)}</span>
                  <div class="config-section-card__titles">
                    <h3 class="config-section-card__title">${v.label}</h3>
                    ${v.description?r`<p class="config-section-card__desc">${v.description}</p>`:m}
                  </div>
                </div>
                <div class="config-section-card__content">
                  ${Le({schema:y,value:n[u],path:[u],hints:e.uiHints,unsupported:i,disabled:e.disabled??!1,showLabel:!1,onPatch:e.onPatch})}
                </div>
              </section>
            `})}
    </div>
  `}const gv=new Set(["title","description","default","nullable"]);function hv(e){return Object.keys(e??{}).filter(n=>!gv.has(n)).length===0}function or(e){const t=e.filter(s=>s!=null),n=t.length!==e.length,i=[];for(const s of t)i.some(a=>Object.is(a,s))||i.push(s);return{enumValues:i,nullable:n}}function lr(e){return!e||typeof e!="object"?{schema:null,unsupportedPaths:["<root>"]}:Nt(e,[])}function Nt(e,t){const n=new Set,i={...e},s=Wn(t)||"<root>";if(e.anyOf||e.oneOf||e.allOf){const l=pv(e,t);return l||{schema:e,unsupportedPaths:[s]}}const a=Array.isArray(e.type)&&e.type.includes("null"),o=Se(e)??(e.properties||e.additionalProperties?"object":void 0);if(i.type=o??e.type,i.nullable=a||e.nullable,i.enum){const{enumValues:l,nullable:d}=or(i.enum);i.enum=l,d&&(i.nullable=!0),l.length===0&&n.add(s)}if(o==="object"){const l=e.properties??{},d={};for(const[h,p]of Object.entries(l)){const u=Nt(p,[...t,h]);u.schema&&(d[h]=u.schema);for(const y of u.unsupportedPaths)n.add(y)}if(i.properties=d,e.additionalProperties===!0)n.add(s);else if(e.additionalProperties===!1)i.additionalProperties=!1;else if(e.additionalProperties&&typeof e.additionalProperties=="object"&&!hv(e.additionalProperties)){const h=Nt(e.additionalProperties,[...t,"*"]);i.additionalProperties=h.schema??e.additionalProperties,h.unsupportedPaths.length>0&&n.add(s)}}else if(o==="array"){const l=Array.isArray(e.items)?e.items[0]:e.items;if(!l)n.add(s);else{const d=Nt(l,[...t,"*"]);i.items=d.schema??l,d.unsupportedPaths.length>0&&n.add(s)}}else o!=="string"&&o!=="number"&&o!=="integer"&&o!=="boolean"&&!i.enum&&n.add(s);return{schema:i,unsupportedPaths:Array.from(n)}}function pv(e,t){if(e.allOf)return null;const n=e.anyOf??e.oneOf;if(!n)return null;const i=[],s=[];let a=!1;for(const l of n){if(!l||typeof l!="object")return null;if(Array.isArray(l.enum)){const{enumValues:d,nullable:h}=or(l.enum);i.push(...d),h&&(a=!0);continue}if("const"in l){if(l.const==null){a=!0;continue}i.push(l.const);continue}if(Se(l)==="null"){a=!0;continue}s.push(l)}if(i.length>0&&s.length===0){const l=[];for(const d of i)l.some(h=>Object.is(h,d))||l.push(d);return{schema:{...e,enum:l,nullable:a,anyOf:void 0,oneOf:void 0,allOf:void 0},unsupportedPaths:[]}}if(s.length===1){const l=Nt(s[0],t);return l.schema&&(l.schema.nullable=a||l.schema.nullable),l}const o=new Set(["string","number","integer","boolean"]);return s.length>0&&i.length===0&&s.every(l=>l.type&&o.has(String(l.type)))?{schema:{...e,nullable:a},unsupportedPaths:[]}:null}function vv(e,t){let n=e;for(const i of t){if(!n)return null;const s=Se(n);if(s==="object"){const a=n.properties??{};if(typeof i=="string"&&a[i]){n=a[i];continue}const o=n.additionalProperties;if(typeof i=="string"&&o&&typeof o=="object"){n=o;continue}return null}if(s==="array"){if(typeof i!="number")return null;n=(Array.isArray(n.items)?n.items[0]:n.items)??null;continue}return null}return n}function mv(e,t){const i=(e.channels??{})[t],s=e[t];return(i&&typeof i=="object"?i:null)??(s&&typeof s=="object"?s:null)??{}}const bv=["groupPolicy","streamMode","dmPolicy"];function yv(e){if(e==null)return"n/a";if(typeof e=="string"||typeof e=="number"||typeof e=="boolean")return String(e);try{return JSON.stringify(e)}catch{return"n/a"}}function wv(e){const t=bv.flatMap(n=>n in e?[[n,e[n]]]:[]);return t.length===0?null:r`
    <div class="status-list" style="margin-top: 12px;">
      ${t.map(([n,i])=>r`
          <div>
            <span class="label">${n}</span>
            <span>${yv(i)}</span>
          </div>
        `)}
    </div>
  `}function $v(e){const t=lr(e.schema),n=t.schema;if(!n)return r`
      <div class="callout danger">Schema unavailable. Use Raw.</div>
    `;const i=vv(n,["channels",e.channelId]);if(!i)return r`
      <div class="callout danger">Channel config schema unavailable.</div>
    `;const s=e.configValue??{},a=mv(s,e.channelId);return r`
    <div class="config-form">
      ${Le({schema:i,value:a,path:["channels",e.channelId],hints:e.uiHints,unsupported:new Set(t.unsupportedPaths),disabled:e.disabled,showLabel:!1,onPatch:e.onPatch})}
    </div>
    ${wv(a)}
  `}function Re(e){const{channelId:t,props:n}=e,i=n.configSaving||n.configSchemaLoading;return r`
    <div style="margin-top: 16px;">
      ${n.configSchemaLoading?r`
              <div class="muted">Loading config schema…</div>
            `:$v({channelId:t,configValue:n.configForm,schema:n.configSchema,uiHints:n.configUiHints,disabled:i,onPatch:n.onConfigPatch})}
      <div class="row" style="margin-top: 12px;">
        <button
          class="btn primary"
          ?disabled=${i||!n.configFormDirty}
          @click=${()=>n.onConfigSave()}
        >
          ${n.configSaving?"Saving…":"Save"}
        </button>
        <button
          class="btn"
          ?disabled=${i}
          @click=${()=>n.onConfigReload()}
        >
          Reload
        </button>
      </div>
    </div>
  `}function kv(e){const{props:t,discord:n,accountCountLabel:i}=e;return r`
    <div class="card">
      <div class="card-title">Discord</div>
      <div class="card-sub">Bot status and channel configuration.</div>
      ${i}

      <div class="status-list" style="margin-top: 16px;">
        <div>
          <span class="label">Configured</span>
          <span>${n?.configured?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Running</span>
          <span>${n?.running?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Last start</span>
          <span>${n?.lastStartAt?U(n.lastStartAt):"n/a"}</span>
        </div>
        <div>
          <span class="label">Last probe</span>
          <span>${n?.lastProbeAt?U(n.lastProbeAt):"n/a"}</span>
        </div>
      </div>

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${n?.probe?r`<div class="callout" style="margin-top: 12px;">
            Probe ${n.probe.ok?"ok":"failed"} ·
            ${n.probe.status??""} ${n.probe.error??""}
          </div>`:m}

      ${Re({channelId:"discord",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Probe
        </button>
      </div>
    </div>
  `}function Av(e){const{props:t,googleChat:n,accountCountLabel:i}=e;return r`
    <div class="card">
      <div class="card-title">Google Chat</div>
      <div class="card-sub">Chat API webhook status and channel configuration.</div>
      ${i}

      <div class="status-list" style="margin-top: 16px;">
        <div>
          <span class="label">Configured</span>
          <span>${n?n.configured?"Yes":"No":"n/a"}</span>
        </div>
        <div>
          <span class="label">Running</span>
          <span>${n?n.running?"Yes":"No":"n/a"}</span>
        </div>
        <div>
          <span class="label">Credential</span>
          <span>${n?.credentialSource??"n/a"}</span>
        </div>
        <div>
          <span class="label">Audience</span>
          <span>
            ${n?.audienceType?`${n.audienceType}${n.audience?` · ${n.audience}`:""}`:"n/a"}
          </span>
        </div>
        <div>
          <span class="label">Last start</span>
          <span>${n?.lastStartAt?U(n.lastStartAt):"n/a"}</span>
        </div>
        <div>
          <span class="label">Last probe</span>
          <span>${n?.lastProbeAt?U(n.lastProbeAt):"n/a"}</span>
        </div>
      </div>

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${n?.probe?r`<div class="callout" style="margin-top: 12px;">
            Probe ${n.probe.ok?"ok":"failed"} ·
            ${n.probe.status??""} ${n.probe.error??""}
          </div>`:m}

      ${Re({channelId:"googlechat",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Probe
        </button>
      </div>
    </div>
  `}function Sv(e){const{props:t,imessage:n,accountCountLabel:i}=e;return r`
    <div class="card">
      <div class="card-title">iMessage</div>
      <div class="card-sub">macOS bridge status and channel configuration.</div>
      ${i}

      <div class="status-list" style="margin-top: 16px;">
        <div>
          <span class="label">Configured</span>
          <span>${n?.configured?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Running</span>
          <span>${n?.running?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Last start</span>
          <span>${n?.lastStartAt?U(n.lastStartAt):"n/a"}</span>
        </div>
        <div>
          <span class="label">Last probe</span>
          <span>${n?.lastProbeAt?U(n.lastProbeAt):"n/a"}</span>
        </div>
      </div>

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${n?.probe?r`<div class="callout" style="margin-top: 12px;">
            Probe ${n.probe.ok?"ok":"failed"} ·
            ${n.probe.error??""}
          </div>`:m}

      ${Re({channelId:"imessage",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Probe
        </button>
      </div>
    </div>
  `}function co(e){return e?e.length<=20?e:`${e.slice(0,8)}...${e.slice(-8)}`:"n/a"}function xv(e){const{props:t,nostr:n,nostrAccounts:i,accountCountLabel:s,profileFormState:a,profileFormCallbacks:o,onEditProfile:l}=e,d=i[0],h=n?.configured??d?.configured??!1,p=n?.running??d?.running??!1,u=n?.publicKey??d?.publicKey,y=n?.lastStartAt??d?.lastStartAt??null,v=n?.lastError??d?.lastError??null,$=i.length>1,g=a!=null,w=C=>{const L=C.publicKey,x=C.profile,T=x?.displayName??x?.name??C.name??C.accountId;return r`
      <div class="account-card">
        <div class="account-card-header">
          <div class="account-card-title">${T}</div>
          <div class="account-card-id">${C.accountId}</div>
        </div>
        <div class="status-list account-card-status">
          <div>
            <span class="label">Running</span>
            <span>${C.running?"Yes":"No"}</span>
          </div>
          <div>
            <span class="label">Configured</span>
            <span>${C.configured?"Yes":"No"}</span>
          </div>
          <div>
            <span class="label">Public Key</span>
            <span class="monospace" title="${L??""}">${co(L)}</span>
          </div>
          <div>
            <span class="label">Last inbound</span>
            <span>${C.lastInboundAt?U(C.lastInboundAt):"n/a"}</span>
          </div>
          ${C.lastError?r`
                <div class="account-card-error">${C.lastError}</div>
              `:m}
        </div>
      </div>
    `},_=()=>{if(g&&o)return mf({state:a,callbacks:o,accountId:i[0]?.accountId??"default"});const C=d?.profile??n?.profile,{name:L,displayName:x,about:T,picture:I,nip05:N}=C??{},fe=L||x||T||I||N;return r`
      <div style="margin-top: 16px; padding: 12px; background: var(--bg-secondary); border-radius: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <div style="font-weight: 500;">Profile</div>
          ${h?r`
                <button
                  class="btn btn-sm"
                  @click=${l}
                  style="font-size: 12px; padding: 4px 8px;"
                >
                  Edit Profile
                </button>
              `:m}
        </div>
        ${fe?r`
              <div class="status-list">
                ${I?r`
                      <div style="margin-bottom: 8px;">
                        <img
                          src=${I}
                          alt="Profile picture"
                          style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover; border: 2px solid var(--border-color);"
                          @error=${G=>{G.target.style.display="none"}}
                        />
                      </div>
                    `:m}
                ${L?r`<div><span class="label">Name</span><span>${L}</span></div>`:m}
                ${x?r`<div><span class="label">Display Name</span><span>${x}</span></div>`:m}
                ${T?r`<div><span class="label">About</span><span style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;">${T}</span></div>`:m}
                ${N?r`<div><span class="label">NIP-05</span><span>${N}</span></div>`:m}
              </div>
            `:r`
                <div style="color: var(--text-muted); font-size: 13px">
                  No profile set. Click "Edit Profile" to add your name, bio, and avatar.
                </div>
              `}
      </div>
    `};return r`
    <div class="card">
      <div class="card-title">Nostr</div>
      <div class="card-sub">Decentralized DMs via Nostr relays (NIP-04).</div>
      ${s}

      ${$?r`
            <div class="account-card-list">
              ${i.map(C=>w(C))}
            </div>
          `:r`
            <div class="status-list" style="margin-top: 16px;">
              <div>
                <span class="label">Configured</span>
                <span>${h?"Yes":"No"}</span>
              </div>
              <div>
                <span class="label">Running</span>
                <span>${p?"Yes":"No"}</span>
              </div>
              <div>
                <span class="label">Public Key</span>
                <span class="monospace" title="${u??""}"
                  >${co(u)}</span
                >
              </div>
              <div>
                <span class="label">Last start</span>
                <span>${y?U(y):"n/a"}</span>
              </div>
            </div>
          `}

      ${v?r`<div class="callout danger" style="margin-top: 12px;">${v}</div>`:m}

      ${_()}

      ${Re({channelId:"nostr",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!1)}>Refresh</button>
      </div>
    </div>
  `}function _v(e){if(!e&&e!==0)return"n/a";const t=Math.round(e/1e3);if(t<60)return`${t}s`;const n=Math.round(t/60);return n<60?`${n}m`:`${Math.round(n/60)}h`}function Cv(e,t){const n=t.snapshot,i=n?.channels;if(!n||!i)return!1;const s=i[e],a=typeof s?.configured=="boolean"&&s.configured,o=typeof s?.running=="boolean"&&s.running,l=typeof s?.connected=="boolean"&&s.connected,h=(n.channelAccounts?.[e]??[]).some(p=>p.configured||p.running||p.connected);return a||o||l||h}function Ev(e,t){return t?.[e]?.length??0}function rr(e,t){const n=Ev(e,t);return n<2?m:r`<div class="account-count">Accounts (${n})</div>`}function Tv(e){const{props:t,signal:n,accountCountLabel:i}=e;return r`
    <div class="card">
      <div class="card-title">Signal</div>
      <div class="card-sub">signal-cli status and channel configuration.</div>
      ${i}

      <div class="status-list" style="margin-top: 16px;">
        <div>
          <span class="label">Configured</span>
          <span>${n?.configured?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Running</span>
          <span>${n?.running?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Base URL</span>
          <span>${n?.baseUrl??"n/a"}</span>
        </div>
        <div>
          <span class="label">Last start</span>
          <span>${n?.lastStartAt?U(n.lastStartAt):"n/a"}</span>
        </div>
        <div>
          <span class="label">Last probe</span>
          <span>${n?.lastProbeAt?U(n.lastProbeAt):"n/a"}</span>
        </div>
      </div>

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${n?.probe?r`<div class="callout" style="margin-top: 12px;">
            Probe ${n.probe.ok?"ok":"failed"} ·
            ${n.probe.status??""} ${n.probe.error??""}
          </div>`:m}

      ${Re({channelId:"signal",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Probe
        </button>
      </div>
    </div>
  `}function Lv(e){const{props:t,slack:n,accountCountLabel:i}=e;return r`
    <div class="card">
      <div class="card-title">Slack</div>
      <div class="card-sub">Socket mode status and channel configuration.</div>
      ${i}

      <div class="status-list" style="margin-top: 16px;">
        <div>
          <span class="label">Configured</span>
          <span>${n?.configured?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Running</span>
          <span>${n?.running?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Last start</span>
          <span>${n?.lastStartAt?U(n.lastStartAt):"n/a"}</span>
        </div>
        <div>
          <span class="label">Last probe</span>
          <span>${n?.lastProbeAt?U(n.lastProbeAt):"n/a"}</span>
        </div>
      </div>

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${n?.probe?r`<div class="callout" style="margin-top: 12px;">
            Probe ${n.probe.ok?"ok":"failed"} ·
            ${n.probe.status??""} ${n.probe.error??""}
          </div>`:m}

      ${Re({channelId:"slack",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Probe
        </button>
      </div>
    </div>
  `}function Iv(e){const{props:t,telegram:n,telegramAccounts:i,accountCountLabel:s}=e,a=i.length>1,o=l=>{const h=l.probe?.bot?.username,p=l.name||l.accountId;return r`
      <div class="account-card">
        <div class="account-card-header">
          <div class="account-card-title">
            ${h?`@${h}`:p}
          </div>
          <div class="account-card-id">${l.accountId}</div>
        </div>
        <div class="status-list account-card-status">
          <div>
            <span class="label">Running</span>
            <span>${l.running?"Yes":"No"}</span>
          </div>
          <div>
            <span class="label">Configured</span>
            <span>${l.configured?"Yes":"No"}</span>
          </div>
          <div>
            <span class="label">Last inbound</span>
            <span>${l.lastInboundAt?U(l.lastInboundAt):"n/a"}</span>
          </div>
          ${l.lastError?r`
                <div class="account-card-error">
                  ${l.lastError}
                </div>
              `:m}
        </div>
      </div>
    `};return r`
    <div class="card">
      <div class="card-title">Telegram</div>
      <div class="card-sub">Bot status and channel configuration.</div>
      ${s}

      ${a?r`
            <div class="account-card-list">
              ${i.map(l=>o(l))}
            </div>
          `:r`
            <div class="status-list" style="margin-top: 16px;">
              <div>
                <span class="label">Configured</span>
                <span>${n?.configured?"Yes":"No"}</span>
              </div>
              <div>
                <span class="label">Running</span>
                <span>${n?.running?"Yes":"No"}</span>
              </div>
              <div>
                <span class="label">Mode</span>
                <span>${n?.mode??"n/a"}</span>
              </div>
              <div>
                <span class="label">Last start</span>
                <span>${n?.lastStartAt?U(n.lastStartAt):"n/a"}</span>
              </div>
              <div>
                <span class="label">Last probe</span>
                <span>${n?.lastProbeAt?U(n.lastProbeAt):"n/a"}</span>
              </div>
            </div>
          `}

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${n?.probe?r`<div class="callout" style="margin-top: 12px;">
            Probe ${n.probe.ok?"ok":"failed"} ·
            ${n.probe.status??""} ${n.probe.error??""}
          </div>`:m}

      ${Re({channelId:"telegram",props:t})}

      <div class="row" style="margin-top: 12px;">
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Probe
        </button>
      </div>
    </div>
  `}function Rv(e){const{props:t,whatsapp:n,accountCountLabel:i}=e;return r`
    <div class="card">
      <div class="card-title">WhatsApp</div>
      <div class="card-sub">Link WhatsApp Web and monitor connection health.</div>
      ${i}

      <div class="status-list" style="margin-top: 16px;">
        <div>
          <span class="label">Configured</span>
          <span>${n?.configured?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Linked</span>
          <span>${n?.linked?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Running</span>
          <span>${n?.running?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Connected</span>
          <span>${n?.connected?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Last connect</span>
          <span>
            ${n?.lastConnectedAt?U(n.lastConnectedAt):"n/a"}
          </span>
        </div>
        <div>
          <span class="label">Last message</span>
          <span>
            ${n?.lastMessageAt?U(n.lastMessageAt):"n/a"}
          </span>
        </div>
        <div>
          <span class="label">Auth age</span>
          <span>
            ${n?.authAgeMs!=null?_v(n.authAgeMs):"n/a"}
          </span>
        </div>
      </div>

      ${n?.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${n.lastError}
          </div>`:m}

      ${t.whatsappMessage?r`<div class="callout" style="margin-top: 12px;">
            ${t.whatsappMessage}
          </div>`:m}

      ${t.whatsappQrDataUrl?r`<div class="qr-wrap">
            <img src=${t.whatsappQrDataUrl} alt="WhatsApp QR" />
          </div>`:m}

      <div class="row" style="margin-top: 14px; flex-wrap: wrap;">
        <button
          class="btn primary"
          ?disabled=${t.whatsappBusy}
          @click=${()=>t.onWhatsAppStart(!1)}
        >
          ${t.whatsappBusy?"Working…":"Show QR"}
        </button>
        <button
          class="btn"
          ?disabled=${t.whatsappBusy}
          @click=${()=>t.onWhatsAppStart(!0)}
        >
          Relink
        </button>
        <button
          class="btn"
          ?disabled=${t.whatsappBusy}
          @click=${()=>t.onWhatsAppWait()}
        >
          Wait for scan
        </button>
        <button
          class="btn danger"
          ?disabled=${t.whatsappBusy}
          @click=${()=>t.onWhatsAppLogout()}
        >
          Logout
        </button>
        <button class="btn" @click=${()=>t.onRefresh(!0)}>
          Refresh
        </button>
      </div>

      ${Re({channelId:"whatsapp",props:t})}
    </div>
  `}function Mv(e){const t=e.snapshot?.channels,n=t?.whatsapp??void 0,i=t?.telegram??void 0,s=t?.discord??null,a=t?.googlechat??null,o=t?.slack??null,l=t?.signal??null,d=t?.imessage??null,h=t?.nostr??null,u=Pv(e.snapshot).map((y,v)=>({key:y,enabled:Cv(y,e),order:v})).toSorted((y,v)=>y.enabled!==v.enabled?y.enabled?-1:1:y.order-v.order);return r`
    <section class="grid grid-cols-2">
      ${u.map(y=>Fv(y.key,e,{whatsapp:n,telegram:i,discord:s,googlechat:a,slack:o,signal:l,imessage:d,nostr:h,channelAccounts:e.snapshot?.channelAccounts??null}))}
    </section>

    <section class="card" style="margin-top: 18px;">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Channel health</div>
          <div class="card-sub">Channel status snapshots from the gateway.</div>
        </div>
        <div class="muted">${e.lastSuccessAt?U(e.lastSuccessAt):"n/a"}</div>
      </div>
      ${e.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${e.lastError}
          </div>`:m}
      <pre class="code-block" style="margin-top: 12px;">
${e.snapshot?JSON.stringify(e.snapshot,null,2):"No snapshot yet."}
      </pre>
    </section>
  `}function Pv(e){return e?.channelMeta?.length?e.channelMeta.map(t=>t.id):e?.channelOrder?.length?e.channelOrder:["whatsapp","telegram","discord","googlechat","slack","signal","imessage","nostr"]}function Fv(e,t,n){const i=rr(e,n.channelAccounts);switch(e){case"whatsapp":return Rv({props:t,whatsapp:n.whatsapp,accountCountLabel:i});case"telegram":return Iv({props:t,telegram:n.telegram,telegramAccounts:n.channelAccounts?.telegram??[],accountCountLabel:i});case"discord":return kv({props:t,discord:n.discord,accountCountLabel:i});case"googlechat":return Av({props:t,googleChat:n.googlechat,accountCountLabel:i});case"slack":return Lv({props:t,slack:n.slack,accountCountLabel:i});case"signal":return Tv({props:t,signal:n.signal,accountCountLabel:i});case"imessage":return Sv({props:t,imessage:n.imessage,accountCountLabel:i});case"nostr":{const s=n.channelAccounts?.nostr??[],a=s[0],o=a?.accountId??"default",l=a?.profile??null,d=t.nostrProfileAccountId===o?t.nostrProfileFormState:null,h=d?{onFieldChange:t.onNostrProfileFieldChange,onSave:t.onNostrProfileSave,onImport:t.onNostrProfileImport,onCancel:t.onNostrProfileCancel,onToggleAdvanced:t.onNostrProfileToggleAdvanced}:null;return xv({props:t,nostr:n.nostr,nostrAccounts:s,accountCountLabel:i,profileFormState:d,profileFormCallbacks:h,onEditProfile:()=>t.onNostrProfileEdit(o,l)})}default:return Nv(e,t,n.channelAccounts??{})}}function Nv(e,t,n){const i=Dv(t.snapshot,e),s=t.snapshot?.channels?.[e],a=typeof s?.configured=="boolean"?s.configured:void 0,o=typeof s?.running=="boolean"?s.running:void 0,l=typeof s?.connected=="boolean"?s.connected:void 0,d=typeof s?.lastError=="string"?s.lastError:void 0,h=n[e]??[],p=rr(e,n);return r`
    <div class="card">
      <div class="card-title">${i}</div>
      <div class="card-sub">Channel status and configuration.</div>
      ${p}

      ${h.length>0?r`
            <div class="account-card-list">
              ${h.map(u=>zv(u))}
            </div>
          `:r`
            <div class="status-list" style="margin-top: 16px;">
              <div>
                <span class="label">Configured</span>
                <span>${a==null?"n/a":a?"Yes":"No"}</span>
              </div>
              <div>
                <span class="label">Running</span>
                <span>${o==null?"n/a":o?"Yes":"No"}</span>
              </div>
              <div>
                <span class="label">Connected</span>
                <span>${l==null?"n/a":l?"Yes":"No"}</span>
              </div>
            </div>
          `}

      ${d?r`<div class="callout danger" style="margin-top: 12px;">
            ${d}
          </div>`:m}

      ${Re({channelId:e,props:t})}
    </div>
  `}function Ov(e){return e?.channelMeta?.length?Object.fromEntries(e.channelMeta.map(t=>[t.id,t])):{}}function Dv(e,t){return Ov(e)[t]?.label??e?.channelLabels?.[t]??t}const Bv=600*1e3;function cr(e){return e.lastInboundAt?Date.now()-e.lastInboundAt<Bv:!1}function Uv(e){return e.running?"Yes":cr(e)?"Active":"No"}function Kv(e){return e.connected===!0?"Yes":e.connected===!1?"No":cr(e)?"Active":"n/a"}function zv(e){const t=Uv(e),n=Kv(e);return r`
    <div class="account-card">
      <div class="account-card-header">
        <div class="account-card-title">${e.name||e.accountId}</div>
        <div class="account-card-id">${e.accountId}</div>
      </div>
      <div class="status-list account-card-status">
        <div>
          <span class="label">Running</span>
          <span>${t}</span>
        </div>
        <div>
          <span class="label">Configured</span>
          <span>${e.configured?"Yes":"No"}</span>
        </div>
        <div>
          <span class="label">Connected</span>
          <span>${n}</span>
        </div>
        <div>
          <span class="label">Last inbound</span>
          <span>${e.lastInboundAt?U(e.lastInboundAt):"n/a"}</span>
        </div>
        ${e.lastError?r`
              <div class="account-card-error">
                ${e.lastError}
              </div>
            `:m}
      </div>
    </div>
  `}const Ot=(e,t)=>{const n=e._$AN;if(n===void 0)return!1;for(const i of n)i._$AO?.(t,!1),Ot(i,t);return!0},Ln=e=>{let t,n;do{if((t=e._$AM)===void 0)break;n=t._$AN,n.delete(e),e=t}while(n?.size===0)},dr=e=>{for(let t;t=e._$AM;e=t){let n=t._$AN;if(n===void 0)t._$AN=n=new Set;else if(n.has(e))break;n.add(e),Gv(t)}};function Hv(e){this._$AN!==void 0?(Ln(this),this._$AM=e,dr(this)):this._$AM=e}function jv(e,t=!1,n=0){const i=this._$AH,s=this._$AN;if(s!==void 0&&s.size!==0)if(t)if(Array.isArray(i))for(let a=n;a<i.length;a++)Ot(i[a],!1),Ln(i[a]);else i!=null&&(Ot(i,!1),Ln(i));else Ot(this,e)}const Gv=e=>{e.type==Is.CHILD&&(e._$AP??=jv,e._$AQ??=Hv)};class Wv extends Ms{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,n,i){super._$AT(t,n,i),dr(this),this.isConnected=t._$AU}_$AO(t,n=!0){t!==this.isConnected&&(this.isConnected=t,t?this.reconnected?.():this.disconnected?.()),n&&(Ot(this,t),Ln(this))}setValue(t){if(op(this._$Ct))this._$Ct._$AI(t,this);else{const n=[...this._$Ct._$AH];n[this._$Ci]=t,this._$Ct._$AI(n,this,0)}}disconnected(){}reconnected(){}}const ki=new WeakMap,qv=Rs(class extends Wv{render(e){return m}update(e,[t]){const n=t!==this.G;return n&&this.G!==void 0&&this.rt(void 0),(n||this.lt!==this.ct)&&(this.G=t,this.ht=e.options?.host,this.rt(this.ct=e.element)),m}rt(e){if(this.isConnected||(e=void 0),typeof this.G=="function"){const t=this.ht??globalThis;let n=ki.get(t);n===void 0&&(n=new WeakMap,ki.set(t,n)),n.get(this.G)!==void 0&&this.G.call(this.ht,void 0),n.set(this.G,e),e!==void 0&&this.G.call(this.ht,e)}else this.G.value=e}get lt(){return typeof this.G=="function"?ki.get(this.ht??globalThis)?.get(this.G):this.G?.value}disconnected(){this.lt===this.ct&&this.rt(void 0)}reconnected(){this.rt(this.ct)}});class Vi extends Ms{constructor(t){if(super(t),this.it=m,t.type!==Is.CHILD)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(t){if(t===m||t==null)return this._t=void 0,this.it=t;if(t===Ne)return t;if(typeof t!="string")throw Error(this.constructor.directiveName+"() called with a non-string value");if(t===this.it)return this._t;this.it=t;const n=[t];return n.raw=n,this._t={_$litType$:this.constructor.resultType,strings:n,values:[]}}}Vi.directiveName="unsafeHTML",Vi.resultType=1;const Yi=Rs(Vi);const{entries:ur,setPrototypeOf:uo,isFrozen:Vv,getPrototypeOf:Yv,getOwnPropertyDescriptor:Qv}=Object;let{freeze:ie,seal:ue,create:Qi}=Object,{apply:Ji,construct:Zi}=typeof Reflect<"u"&&Reflect;ie||(ie=function(t){return t});ue||(ue=function(t){return t});Ji||(Ji=function(t,n){for(var i=arguments.length,s=new Array(i>2?i-2:0),a=2;a<i;a++)s[a-2]=arguments[a];return t.apply(n,s)});Zi||(Zi=function(t){for(var n=arguments.length,i=new Array(n>1?n-1:0),s=1;s<n;s++)i[s-1]=arguments[s];return new t(...i)});const gn=se(Array.prototype.forEach),Jv=se(Array.prototype.lastIndexOf),fo=se(Array.prototype.pop),kt=se(Array.prototype.push),Zv=se(Array.prototype.splice),An=se(String.prototype.toLowerCase),Ai=se(String.prototype.toString),Si=se(String.prototype.match),At=se(String.prototype.replace),Xv=se(String.prototype.indexOf),em=se(String.prototype.trim),he=se(Object.prototype.hasOwnProperty),te=se(RegExp.prototype.test),St=tm(TypeError);function se(e){return function(t){t instanceof RegExp&&(t.lastIndex=0);for(var n=arguments.length,i=new Array(n>1?n-1:0),s=1;s<n;s++)i[s-1]=arguments[s];return Ji(e,t,i)}}function tm(e){return function(){for(var t=arguments.length,n=new Array(t),i=0;i<t;i++)n[i]=arguments[i];return Zi(e,n)}}function F(e,t){let n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:An;uo&&uo(e,null);let i=t.length;for(;i--;){let s=t[i];if(typeof s=="string"){const a=n(s);a!==s&&(Vv(t)||(t[i]=a),s=a)}e[s]=!0}return e}function nm(e){for(let t=0;t<e.length;t++)he(e,t)||(e[t]=null);return e}function ke(e){const t=Qi(null);for(const[n,i]of ur(e))he(e,n)&&(Array.isArray(i)?t[n]=nm(i):i&&typeof i=="object"&&i.constructor===Object?t[n]=ke(i):t[n]=i);return t}function xt(e,t){for(;e!==null;){const i=Qv(e,t);if(i){if(i.get)return se(i.get);if(typeof i.value=="function")return se(i.value)}e=Yv(e)}function n(){return null}return n}const go=ie(["a","abbr","acronym","address","area","article","aside","audio","b","bdi","bdo","big","blink","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","content","data","datalist","dd","decorator","del","details","dfn","dialog","dir","div","dl","dt","element","em","fieldset","figcaption","figure","font","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","img","input","ins","kbd","label","legend","li","main","map","mark","marquee","menu","menuitem","meter","nav","nobr","ol","optgroup","option","output","p","picture","pre","progress","q","rp","rt","ruby","s","samp","search","section","select","shadow","slot","small","source","spacer","span","strike","strong","style","sub","summary","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","tr","track","tt","u","ul","var","video","wbr"]),xi=ie(["svg","a","altglyph","altglyphdef","altglyphitem","animatecolor","animatemotion","animatetransform","circle","clippath","defs","desc","ellipse","enterkeyhint","exportparts","filter","font","g","glyph","glyphref","hkern","image","inputmode","line","lineargradient","marker","mask","metadata","mpath","part","path","pattern","polygon","polyline","radialgradient","rect","stop","style","switch","symbol","text","textpath","title","tref","tspan","view","vkern"]),_i=ie(["feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feDropShadow","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence"]),im=ie(["animate","color-profile","cursor","discard","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignobject","hatch","hatchpath","mesh","meshgradient","meshpatch","meshrow","missing-glyph","script","set","solidcolor","unknown","use"]),Ci=ie(["math","menclose","merror","mfenced","mfrac","mglyph","mi","mlabeledtr","mmultiscripts","mn","mo","mover","mpadded","mphantom","mroot","mrow","ms","mspace","msqrt","mstyle","msub","msup","msubsup","mtable","mtd","mtext","mtr","munder","munderover","mprescripts"]),sm=ie(["maction","maligngroup","malignmark","mlongdiv","mscarries","mscarry","msgroup","mstack","msline","msrow","semantics","annotation","annotation-xml","mprescripts","none"]),ho=ie(["#text"]),po=ie(["accept","action","align","alt","autocapitalize","autocomplete","autopictureinpicture","autoplay","background","bgcolor","border","capture","cellpadding","cellspacing","checked","cite","class","clear","color","cols","colspan","controls","controlslist","coords","crossorigin","datetime","decoding","default","dir","disabled","disablepictureinpicture","disableremoteplayback","download","draggable","enctype","enterkeyhint","exportparts","face","for","headers","height","hidden","high","href","hreflang","id","inert","inputmode","integrity","ismap","kind","label","lang","list","loading","loop","low","max","maxlength","media","method","min","minlength","multiple","muted","name","nonce","noshade","novalidate","nowrap","open","optimum","part","pattern","placeholder","playsinline","popover","popovertarget","popovertargetaction","poster","preload","pubdate","radiogroup","readonly","rel","required","rev","reversed","role","rows","rowspan","spellcheck","scope","selected","shape","size","sizes","slot","span","srclang","start","src","srcset","step","style","summary","tabindex","title","translate","type","usemap","valign","value","width","wrap","xmlns","slot"]),Ei=ie(["accent-height","accumulate","additive","alignment-baseline","amplitude","ascent","attributename","attributetype","azimuth","basefrequency","baseline-shift","begin","bias","by","class","clip","clippathunits","clip-path","clip-rule","color","color-interpolation","color-interpolation-filters","color-profile","color-rendering","cx","cy","d","dx","dy","diffuseconstant","direction","display","divisor","dur","edgemode","elevation","end","exponent","fill","fill-opacity","fill-rule","filter","filterunits","flood-color","flood-opacity","font-family","font-size","font-size-adjust","font-stretch","font-style","font-variant","font-weight","fx","fy","g1","g2","glyph-name","glyphref","gradientunits","gradienttransform","height","href","id","image-rendering","in","in2","intercept","k","k1","k2","k3","k4","kerning","keypoints","keysplines","keytimes","lang","lengthadjust","letter-spacing","kernelmatrix","kernelunitlength","lighting-color","local","marker-end","marker-mid","marker-start","markerheight","markerunits","markerwidth","maskcontentunits","maskunits","max","mask","mask-type","media","method","mode","min","name","numoctaves","offset","operator","opacity","order","orient","orientation","origin","overflow","paint-order","path","pathlength","patterncontentunits","patterntransform","patternunits","points","preservealpha","preserveaspectratio","primitiveunits","r","rx","ry","radius","refx","refy","repeatcount","repeatdur","restart","result","rotate","scale","seed","shape-rendering","slope","specularconstant","specularexponent","spreadmethod","startoffset","stddeviation","stitchtiles","stop-color","stop-opacity","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke","stroke-width","style","surfacescale","systemlanguage","tabindex","tablevalues","targetx","targety","transform","transform-origin","text-anchor","text-decoration","text-rendering","textlength","type","u1","u2","unicode","values","viewbox","visibility","version","vert-adv-y","vert-origin-x","vert-origin-y","width","word-spacing","wrap","writing-mode","xchannelselector","ychannelselector","x","x1","x2","xmlns","y","y1","y2","z","zoomandpan"]),vo=ie(["accent","accentunder","align","bevelled","close","columnsalign","columnlines","columnspan","denomalign","depth","dir","display","displaystyle","encoding","fence","frame","height","href","id","largeop","length","linethickness","lspace","lquote","mathbackground","mathcolor","mathsize","mathvariant","maxsize","minsize","movablelimits","notation","numalign","open","rowalign","rowlines","rowspacing","rowspan","rspace","rquote","scriptlevel","scriptminsize","scriptsizemultiplier","selection","separator","separators","stretchy","subscriptshift","supscriptshift","symmetric","voffset","width","xmlns"]),hn=ie(["xlink:href","xml:id","xlink:title","xml:space","xmlns:xlink"]),am=ue(/\{\{[\w\W]*|[\w\W]*\}\}/gm),om=ue(/<%[\w\W]*|[\w\W]*%>/gm),lm=ue(/\$\{[\w\W]*/gm),rm=ue(/^data-[\-\w.\u00B7-\uFFFF]+$/),cm=ue(/^aria-[\-\w]+$/),fr=ue(/^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp|matrix):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i),dm=ue(/^(?:\w+script|data):/i),um=ue(/[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g),gr=ue(/^html$/i),fm=ue(/^[a-z][.\w]*(-[.\w]+)+$/i);var mo=Object.freeze({__proto__:null,ARIA_ATTR:cm,ATTR_WHITESPACE:um,CUSTOM_ELEMENT:fm,DATA_ATTR:rm,DOCTYPE_NAME:gr,ERB_EXPR:om,IS_ALLOWED_URI:fr,IS_SCRIPT_OR_DATA:dm,MUSTACHE_EXPR:am,TMPLIT_EXPR:lm});const _t={element:1,text:3,progressingInstruction:7,comment:8,document:9},gm=function(){return typeof window>"u"?null:window},hm=function(t,n){if(typeof t!="object"||typeof t.createPolicy!="function")return null;let i=null;const s="data-tt-policy-suffix";n&&n.hasAttribute(s)&&(i=n.getAttribute(s));const a="dompurify"+(i?"#"+i:"");try{return t.createPolicy(a,{createHTML(o){return o},createScriptURL(o){return o}})}catch{return console.warn("TrustedTypes policy "+a+" could not be created."),null}},bo=function(){return{afterSanitizeAttributes:[],afterSanitizeElements:[],afterSanitizeShadowDOM:[],beforeSanitizeAttributes:[],beforeSanitizeElements:[],beforeSanitizeShadowDOM:[],uponSanitizeAttribute:[],uponSanitizeElement:[],uponSanitizeShadowNode:[]}};function hr(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:gm();const t=P=>hr(P);if(t.version="3.3.1",t.removed=[],!e||!e.document||e.document.nodeType!==_t.document||!e.Element)return t.isSupported=!1,t;let{document:n}=e;const i=n,s=i.currentScript,{DocumentFragment:a,HTMLTemplateElement:o,Node:l,Element:d,NodeFilter:h,NamedNodeMap:p=e.NamedNodeMap||e.MozNamedAttrMap,HTMLFormElement:u,DOMParser:y,trustedTypes:v}=e,$=d.prototype,g=xt($,"cloneNode"),w=xt($,"remove"),_=xt($,"nextSibling"),C=xt($,"childNodes"),L=xt($,"parentNode");if(typeof o=="function"){const P=n.createElement("template");P.content&&P.content.ownerDocument&&(n=P.content.ownerDocument)}let x,T="";const{implementation:I,createNodeIterator:N,createDocumentFragment:fe,getElementsByTagName:G}=n,{importNode:Z}=i;let B=bo();t.isSupported=typeof ur=="function"&&typeof L=="function"&&I&&I.createHTMLDocument!==void 0;const{MUSTACHE_EXPR:Ue,ERB_EXPR:le,TMPLIT_EXPR:Me,DATA_ATTR:be,ARIA_ATTR:Js,IS_SCRIPT_OR_DATA:Xt,ATTR_WHITESPACE:Qn,CUSTOM_ELEMENT:Cu}=mo;let{IS_ALLOWED_URI:Zs}=mo,W=null;const Xs=F({},[...go,...xi,..._i,...Ci,...ho]);let Y=null;const ea=F({},[...po,...Ei,...vo,...hn]);let z=Object.seal(Qi(null,{tagNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},allowCustomizedBuiltInElements:{writable:!0,configurable:!1,enumerable:!0,value:!1}})),mt=null,Jn=null;const st=Object.seal(Qi(null,{tagCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeCheck:{writable:!0,configurable:!1,enumerable:!0,value:null}}));let ta=!0,Zn=!0,na=!1,ia=!0,at=!1,en=!0,Ke=!1,Xn=!1,ei=!1,ot=!1,tn=!1,nn=!1,sa=!0,aa=!1;const Eu="user-content-";let ti=!0,bt=!1,lt={},ye=null;const ni=F({},["annotation-xml","audio","colgroup","desc","foreignobject","head","iframe","math","mi","mn","mo","ms","mtext","noembed","noframes","noscript","plaintext","script","style","svg","template","thead","title","video","xmp"]);let oa=null;const la=F({},["audio","video","img","source","image","track"]);let ii=null;const ra=F({},["alt","class","for","id","label","name","pattern","placeholder","role","summary","title","value","style","xmlns"]),sn="http://www.w3.org/1998/Math/MathML",an="http://www.w3.org/2000/svg",xe="http://www.w3.org/1999/xhtml";let rt=xe,si=!1,ai=null;const Tu=F({},[sn,an,xe],Ai);let on=F({},["mi","mo","mn","ms","mtext"]),ln=F({},["annotation-xml"]);const Lu=F({},["title","style","font","a","script"]);let yt=null;const Iu=["application/xhtml+xml","text/html"],Ru="text/html";let j=null,ct=null;const Mu=n.createElement("form"),ca=function(b){return b instanceof RegExp||b instanceof Function},oi=function(){let b=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};if(!(ct&&ct===b)){if((!b||typeof b!="object")&&(b={}),b=ke(b),yt=Iu.indexOf(b.PARSER_MEDIA_TYPE)===-1?Ru:b.PARSER_MEDIA_TYPE,j=yt==="application/xhtml+xml"?Ai:An,W=he(b,"ALLOWED_TAGS")?F({},b.ALLOWED_TAGS,j):Xs,Y=he(b,"ALLOWED_ATTR")?F({},b.ALLOWED_ATTR,j):ea,ai=he(b,"ALLOWED_NAMESPACES")?F({},b.ALLOWED_NAMESPACES,Ai):Tu,ii=he(b,"ADD_URI_SAFE_ATTR")?F(ke(ra),b.ADD_URI_SAFE_ATTR,j):ra,oa=he(b,"ADD_DATA_URI_TAGS")?F(ke(la),b.ADD_DATA_URI_TAGS,j):la,ye=he(b,"FORBID_CONTENTS")?F({},b.FORBID_CONTENTS,j):ni,mt=he(b,"FORBID_TAGS")?F({},b.FORBID_TAGS,j):ke({}),Jn=he(b,"FORBID_ATTR")?F({},b.FORBID_ATTR,j):ke({}),lt=he(b,"USE_PROFILES")?b.USE_PROFILES:!1,ta=b.ALLOW_ARIA_ATTR!==!1,Zn=b.ALLOW_DATA_ATTR!==!1,na=b.ALLOW_UNKNOWN_PROTOCOLS||!1,ia=b.ALLOW_SELF_CLOSE_IN_ATTR!==!1,at=b.SAFE_FOR_TEMPLATES||!1,en=b.SAFE_FOR_XML!==!1,Ke=b.WHOLE_DOCUMENT||!1,ot=b.RETURN_DOM||!1,tn=b.RETURN_DOM_FRAGMENT||!1,nn=b.RETURN_TRUSTED_TYPE||!1,ei=b.FORCE_BODY||!1,sa=b.SANITIZE_DOM!==!1,aa=b.SANITIZE_NAMED_PROPS||!1,ti=b.KEEP_CONTENT!==!1,bt=b.IN_PLACE||!1,Zs=b.ALLOWED_URI_REGEXP||fr,rt=b.NAMESPACE||xe,on=b.MATHML_TEXT_INTEGRATION_POINTS||on,ln=b.HTML_INTEGRATION_POINTS||ln,z=b.CUSTOM_ELEMENT_HANDLING||{},b.CUSTOM_ELEMENT_HANDLING&&ca(b.CUSTOM_ELEMENT_HANDLING.tagNameCheck)&&(z.tagNameCheck=b.CUSTOM_ELEMENT_HANDLING.tagNameCheck),b.CUSTOM_ELEMENT_HANDLING&&ca(b.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)&&(z.attributeNameCheck=b.CUSTOM_ELEMENT_HANDLING.attributeNameCheck),b.CUSTOM_ELEMENT_HANDLING&&typeof b.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements=="boolean"&&(z.allowCustomizedBuiltInElements=b.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements),at&&(Zn=!1),tn&&(ot=!0),lt&&(W=F({},ho),Y=[],lt.html===!0&&(F(W,go),F(Y,po)),lt.svg===!0&&(F(W,xi),F(Y,Ei),F(Y,hn)),lt.svgFilters===!0&&(F(W,_i),F(Y,Ei),F(Y,hn)),lt.mathMl===!0&&(F(W,Ci),F(Y,vo),F(Y,hn))),b.ADD_TAGS&&(typeof b.ADD_TAGS=="function"?st.tagCheck=b.ADD_TAGS:(W===Xs&&(W=ke(W)),F(W,b.ADD_TAGS,j))),b.ADD_ATTR&&(typeof b.ADD_ATTR=="function"?st.attributeCheck=b.ADD_ATTR:(Y===ea&&(Y=ke(Y)),F(Y,b.ADD_ATTR,j))),b.ADD_URI_SAFE_ATTR&&F(ii,b.ADD_URI_SAFE_ATTR,j),b.FORBID_CONTENTS&&(ye===ni&&(ye=ke(ye)),F(ye,b.FORBID_CONTENTS,j)),b.ADD_FORBID_CONTENTS&&(ye===ni&&(ye=ke(ye)),F(ye,b.ADD_FORBID_CONTENTS,j)),ti&&(W["#text"]=!0),Ke&&F(W,["html","head","body"]),W.table&&(F(W,["tbody"]),delete mt.tbody),b.TRUSTED_TYPES_POLICY){if(typeof b.TRUSTED_TYPES_POLICY.createHTML!="function")throw St('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');if(typeof b.TRUSTED_TYPES_POLICY.createScriptURL!="function")throw St('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');x=b.TRUSTED_TYPES_POLICY,T=x.createHTML("")}else x===void 0&&(x=hm(v,s)),x!==null&&typeof T=="string"&&(T=x.createHTML(""));ie&&ie(b),ct=b}},da=F({},[...xi,..._i,...im]),ua=F({},[...Ci,...sm]),Pu=function(b){let E=L(b);(!E||!E.tagName)&&(E={namespaceURI:rt,tagName:"template"});const M=An(b.tagName),K=An(E.tagName);return ai[b.namespaceURI]?b.namespaceURI===an?E.namespaceURI===xe?M==="svg":E.namespaceURI===sn?M==="svg"&&(K==="annotation-xml"||on[K]):!!da[M]:b.namespaceURI===sn?E.namespaceURI===xe?M==="math":E.namespaceURI===an?M==="math"&&ln[K]:!!ua[M]:b.namespaceURI===xe?E.namespaceURI===an&&!ln[K]||E.namespaceURI===sn&&!on[K]?!1:!ua[M]&&(Lu[M]||!da[M]):!!(yt==="application/xhtml+xml"&&ai[b.namespaceURI]):!1},we=function(b){kt(t.removed,{element:b});try{L(b).removeChild(b)}catch{w(b)}},ze=function(b,E){try{kt(t.removed,{attribute:E.getAttributeNode(b),from:E})}catch{kt(t.removed,{attribute:null,from:E})}if(E.removeAttribute(b),b==="is")if(ot||tn)try{we(E)}catch{}else try{E.setAttribute(b,"")}catch{}},fa=function(b){let E=null,M=null;if(ei)b="<remove></remove>"+b;else{const H=Si(b,/^[\r\n\t ]+/);M=H&&H[0]}yt==="application/xhtml+xml"&&rt===xe&&(b='<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>'+b+"</body></html>");const K=x?x.createHTML(b):b;if(rt===xe)try{E=new y().parseFromString(K,yt)}catch{}if(!E||!E.documentElement){E=I.createDocument(rt,"template",null);try{E.documentElement.innerHTML=si?T:K}catch{}}const X=E.body||E.documentElement;return b&&M&&X.insertBefore(n.createTextNode(M),X.childNodes[0]||null),rt===xe?G.call(E,Ke?"html":"body")[0]:Ke?E.documentElement:X},ga=function(b){return N.call(b.ownerDocument||b,b,h.SHOW_ELEMENT|h.SHOW_COMMENT|h.SHOW_TEXT|h.SHOW_PROCESSING_INSTRUCTION|h.SHOW_CDATA_SECTION,null)},li=function(b){return b instanceof u&&(typeof b.nodeName!="string"||typeof b.textContent!="string"||typeof b.removeChild!="function"||!(b.attributes instanceof p)||typeof b.removeAttribute!="function"||typeof b.setAttribute!="function"||typeof b.namespaceURI!="string"||typeof b.insertBefore!="function"||typeof b.hasChildNodes!="function")},ha=function(b){return typeof l=="function"&&b instanceof l};function _e(P,b,E){gn(P,M=>{M.call(t,b,E,ct)})}const pa=function(b){let E=null;if(_e(B.beforeSanitizeElements,b,null),li(b))return we(b),!0;const M=j(b.nodeName);if(_e(B.uponSanitizeElement,b,{tagName:M,allowedTags:W}),en&&b.hasChildNodes()&&!ha(b.firstElementChild)&&te(/<[/\w!]/g,b.innerHTML)&&te(/<[/\w!]/g,b.textContent)||b.nodeType===_t.progressingInstruction||en&&b.nodeType===_t.comment&&te(/<[/\w]/g,b.data))return we(b),!0;if(!(st.tagCheck instanceof Function&&st.tagCheck(M))&&(!W[M]||mt[M])){if(!mt[M]&&ma(M)&&(z.tagNameCheck instanceof RegExp&&te(z.tagNameCheck,M)||z.tagNameCheck instanceof Function&&z.tagNameCheck(M)))return!1;if(ti&&!ye[M]){const K=L(b)||b.parentNode,X=C(b)||b.childNodes;if(X&&K){const H=X.length;for(let ae=H-1;ae>=0;--ae){const Ce=g(X[ae],!0);Ce.__removalCount=(b.__removalCount||0)+1,K.insertBefore(Ce,_(b))}}}return we(b),!0}return b instanceof d&&!Pu(b)||(M==="noscript"||M==="noembed"||M==="noframes")&&te(/<\/no(script|embed|frames)/i,b.innerHTML)?(we(b),!0):(at&&b.nodeType===_t.text&&(E=b.textContent,gn([Ue,le,Me],K=>{E=At(E,K," ")}),b.textContent!==E&&(kt(t.removed,{element:b.cloneNode()}),b.textContent=E)),_e(B.afterSanitizeElements,b,null),!1)},va=function(b,E,M){if(sa&&(E==="id"||E==="name")&&(M in n||M in Mu))return!1;if(!(Zn&&!Jn[E]&&te(be,E))){if(!(ta&&te(Js,E))){if(!(st.attributeCheck instanceof Function&&st.attributeCheck(E,b))){if(!Y[E]||Jn[E]){if(!(ma(b)&&(z.tagNameCheck instanceof RegExp&&te(z.tagNameCheck,b)||z.tagNameCheck instanceof Function&&z.tagNameCheck(b))&&(z.attributeNameCheck instanceof RegExp&&te(z.attributeNameCheck,E)||z.attributeNameCheck instanceof Function&&z.attributeNameCheck(E,b))||E==="is"&&z.allowCustomizedBuiltInElements&&(z.tagNameCheck instanceof RegExp&&te(z.tagNameCheck,M)||z.tagNameCheck instanceof Function&&z.tagNameCheck(M))))return!1}else if(!ii[E]){if(!te(Zs,At(M,Qn,""))){if(!((E==="src"||E==="xlink:href"||E==="href")&&b!=="script"&&Xv(M,"data:")===0&&oa[b])){if(!(na&&!te(Xt,At(M,Qn,"")))){if(M)return!1}}}}}}}return!0},ma=function(b){return b!=="annotation-xml"&&Si(b,Cu)},ba=function(b){_e(B.beforeSanitizeAttributes,b,null);const{attributes:E}=b;if(!E||li(b))return;const M={attrName:"",attrValue:"",keepAttr:!0,allowedAttributes:Y,forceKeepAttr:void 0};let K=E.length;for(;K--;){const X=E[K],{name:H,namespaceURI:ae,value:Ce}=X,dt=j(H),ri=Ce;let Q=H==="value"?ri:em(ri);if(M.attrName=dt,M.attrValue=Q,M.keepAttr=!0,M.forceKeepAttr=void 0,_e(B.uponSanitizeAttribute,b,M),Q=M.attrValue,aa&&(dt==="id"||dt==="name")&&(ze(H,b),Q=Eu+Q),en&&te(/((--!?|])>)|<\/(style|title|textarea)/i,Q)){ze(H,b);continue}if(dt==="attributename"&&Si(Q,"href")){ze(H,b);continue}if(M.forceKeepAttr)continue;if(!M.keepAttr){ze(H,b);continue}if(!ia&&te(/\/>/i,Q)){ze(H,b);continue}at&&gn([Ue,le,Me],wa=>{Q=At(Q,wa," ")});const ya=j(b.nodeName);if(!va(ya,dt,Q)){ze(H,b);continue}if(x&&typeof v=="object"&&typeof v.getAttributeType=="function"&&!ae)switch(v.getAttributeType(ya,dt)){case"TrustedHTML":{Q=x.createHTML(Q);break}case"TrustedScriptURL":{Q=x.createScriptURL(Q);break}}if(Q!==ri)try{ae?b.setAttributeNS(ae,H,Q):b.setAttribute(H,Q),li(b)?we(b):fo(t.removed)}catch{ze(H,b)}}_e(B.afterSanitizeAttributes,b,null)},Fu=function P(b){let E=null;const M=ga(b);for(_e(B.beforeSanitizeShadowDOM,b,null);E=M.nextNode();)_e(B.uponSanitizeShadowNode,E,null),pa(E),ba(E),E.content instanceof a&&P(E.content);_e(B.afterSanitizeShadowDOM,b,null)};return t.sanitize=function(P){let b=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},E=null,M=null,K=null,X=null;if(si=!P,si&&(P="<!-->"),typeof P!="string"&&!ha(P))if(typeof P.toString=="function"){if(P=P.toString(),typeof P!="string")throw St("dirty is not a string, aborting")}else throw St("toString is not a function");if(!t.isSupported)return P;if(Xn||oi(b),t.removed=[],typeof P=="string"&&(bt=!1),bt){if(P.nodeName){const Ce=j(P.nodeName);if(!W[Ce]||mt[Ce])throw St("root node is forbidden and cannot be sanitized in-place")}}else if(P instanceof l)E=fa("<!---->"),M=E.ownerDocument.importNode(P,!0),M.nodeType===_t.element&&M.nodeName==="BODY"||M.nodeName==="HTML"?E=M:E.appendChild(M);else{if(!ot&&!at&&!Ke&&P.indexOf("<")===-1)return x&&nn?x.createHTML(P):P;if(E=fa(P),!E)return ot?null:nn?T:""}E&&ei&&we(E.firstChild);const H=ga(bt?P:E);for(;K=H.nextNode();)pa(K),ba(K),K.content instanceof a&&Fu(K.content);if(bt)return P;if(ot){if(tn)for(X=fe.call(E.ownerDocument);E.firstChild;)X.appendChild(E.firstChild);else X=E;return(Y.shadowroot||Y.shadowrootmode)&&(X=Z.call(i,X,!0)),X}let ae=Ke?E.outerHTML:E.innerHTML;return Ke&&W["!doctype"]&&E.ownerDocument&&E.ownerDocument.doctype&&E.ownerDocument.doctype.name&&te(gr,E.ownerDocument.doctype.name)&&(ae="<!DOCTYPE "+E.ownerDocument.doctype.name+`>
`+ae),at&&gn([Ue,le,Me],Ce=>{ae=At(ae,Ce," ")}),x&&nn?x.createHTML(ae):ae},t.setConfig=function(){let P=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};oi(P),Xn=!0},t.clearConfig=function(){ct=null,Xn=!1},t.isValidAttribute=function(P,b,E){ct||oi({});const M=j(P),K=j(b);return va(M,K,E)},t.addHook=function(P,b){typeof b=="function"&&kt(B[P],b)},t.removeHook=function(P,b){if(b!==void 0){const E=Jv(B[P],b);return E===-1?void 0:Zv(B[P],E,1)[0]}return fo(B[P])},t.removeHooks=function(P){B[P]=[]},t.removeAllHooks=function(){B=bo()},t}var Xi=hr();function Ns(){return{async:!1,breaks:!1,extensions:null,gfm:!0,hooks:null,pedantic:!1,renderer:null,silent:!1,tokenizer:null,walkTokens:null}}var it=Ns();function pr(e){it=e}var Dt={exec:()=>null};function O(e,t=""){let n=typeof e=="string"?e:e.source,i={replace:(s,a)=>{let o=typeof a=="string"?a:a.source;return o=o.replace(ne.caret,"$1"),n=n.replace(s,o),i},getRegex:()=>new RegExp(n,t)};return i}var pm=(()=>{try{return!!new RegExp("(?<=1)(?<!1)")}catch{return!1}})(),ne={codeRemoveIndent:/^(?: {1,4}| {0,3}\t)/gm,outputLinkReplace:/\\([\[\]])/g,indentCodeCompensation:/^(\s+)(?:```)/,beginningSpace:/^\s+/,endingHash:/#$/,startingSpaceChar:/^ /,endingSpaceChar:/ $/,nonSpaceChar:/[^ ]/,newLineCharGlobal:/\n/g,tabCharGlobal:/\t/g,multipleSpaceGlobal:/\s+/g,blankLine:/^[ \t]*$/,doubleBlankLine:/\n[ \t]*\n[ \t]*$/,blockquoteStart:/^ {0,3}>/,blockquoteSetextReplace:/\n {0,3}((?:=+|-+) *)(?=\n|$)/g,blockquoteSetextReplace2:/^ {0,3}>[ \t]?/gm,listReplaceTabs:/^\t+/,listReplaceNesting:/^ {1,4}(?=( {4})*[^ ])/g,listIsTask:/^\[[ xX]\] +\S/,listReplaceTask:/^\[[ xX]\] +/,listTaskCheckbox:/\[[ xX]\]/,anyLine:/\n.*\n/,hrefBrackets:/^<(.*)>$/,tableDelimiter:/[:|]/,tableAlignChars:/^\||\| *$/g,tableRowBlankLine:/\n[ \t]*$/,tableAlignRight:/^ *-+: *$/,tableAlignCenter:/^ *:-+: *$/,tableAlignLeft:/^ *:-+ *$/,startATag:/^<a /i,endATag:/^<\/a>/i,startPreScriptTag:/^<(pre|code|kbd|script)(\s|>)/i,endPreScriptTag:/^<\/(pre|code|kbd|script)(\s|>)/i,startAngleBracket:/^</,endAngleBracket:/>$/,pedanticHrefTitle:/^([^'"]*[^\s])\s+(['"])(.*)\2/,unicodeAlphaNumeric:/[\p{L}\p{N}]/u,escapeTest:/[&<>"']/,escapeReplace:/[&<>"']/g,escapeTestNoEncode:/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,escapeReplaceNoEncode:/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/g,unescapeTest:/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/ig,caret:/(^|[^\[])\^/g,percentDecode:/%25/g,findPipe:/\|/g,splitPipe:/ \|/,slashPipe:/\\\|/g,carriageReturn:/\r\n|\r/g,spaceLine:/^ +$/gm,notSpaceStart:/^\S*/,endingNewline:/\n$/,listItemRegex:e=>new RegExp(`^( {0,3}${e})((?:[	 ][^\\n]*)?(?:\\n|$))`),nextBulletRegex:e=>new RegExp(`^ {0,${Math.min(3,e-1)}}(?:[*+-]|\\d{1,9}[.)])((?:[ 	][^\\n]*)?(?:\\n|$))`),hrRegex:e=>new RegExp(`^ {0,${Math.min(3,e-1)}}((?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$)`),fencesBeginRegex:e=>new RegExp(`^ {0,${Math.min(3,e-1)}}(?:\`\`\`|~~~)`),headingBeginRegex:e=>new RegExp(`^ {0,${Math.min(3,e-1)}}#`),htmlBeginRegex:e=>new RegExp(`^ {0,${Math.min(3,e-1)}}<(?:[a-z].*>|!--)`,"i")},vm=/^(?:[ \t]*(?:\n|$))+/,mm=/^((?: {4}| {0,3}\t)[^\n]+(?:\n(?:[ \t]*(?:\n|$))*)?)+/,bm=/^ {0,3}(`{3,}(?=[^`\n]*(?:\n|$))|~{3,})([^\n]*)(?:\n|$)(?:|([\s\S]*?)(?:\n|$))(?: {0,3}\1[~`]* *(?=\n|$)|$)/,Qt=/^ {0,3}((?:-[\t ]*){3,}|(?:_[ \t]*){3,}|(?:\*[ \t]*){3,})(?:\n+|$)/,ym=/^ {0,3}(#{1,6})(?=\s|$)(.*)(?:\n+|$)/,Os=/(?:[*+-]|\d{1,9}[.)])/,vr=/^(?!bull |blockCode|fences|blockquote|heading|html|table)((?:.|\n(?!\s*?\n|bull |blockCode|fences|blockquote|heading|html|table))+?)\n {0,3}(=+|-+) *(?:\n+|$)/,mr=O(vr).replace(/bull/g,Os).replace(/blockCode/g,/(?: {4}| {0,3}\t)/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).replace(/\|table/g,"").getRegex(),wm=O(vr).replace(/bull/g,Os).replace(/blockCode/g,/(?: {4}| {0,3}\t)/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).replace(/table/g,/ {0,3}\|?(?:[:\- ]*\|)+[\:\- ]*\n/).getRegex(),Ds=/^([^\n]+(?:\n(?!hr|heading|lheading|blockquote|fences|list|html|table| +\n)[^\n]+)*)/,$m=/^[^\n]+/,Bs=/(?!\s*\])(?:\\[\s\S]|[^\[\]\\])+/,km=O(/^ {0,3}\[(label)\]: *(?:\n[ \t]*)?([^<\s][^\s]*|<.*?>)(?:(?: +(?:\n[ \t]*)?| *\n[ \t]*)(title))? *(?:\n+|$)/).replace("label",Bs).replace("title",/(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/).getRegex(),Am=O(/^( {0,3}bull)([ \t][^\n]+?)?(?:\n|$)/).replace(/bull/g,Os).getRegex(),qn="address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul",Us=/<!--(?:-?>|[\s\S]*?(?:-->|$))/,Sm=O("^ {0,3}(?:<(script|pre|style|textarea)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?(?:\\?>\\n*|$)|<![A-Z][\\s\\S]*?(?:>\\n*|$)|<!\\[CDATA\\[[\\s\\S]*?(?:\\]\\]>\\n*|$)|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|<(?!script|pre|style|textarea)([a-z][\\w-]*)(?:attribute)*? */?>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|</(?!script|pre|style|textarea)[a-z][\\w-]*\\s*>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$))","i").replace("comment",Us).replace("tag",qn).replace("attribute",/ +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(),br=O(Ds).replace("hr",Qt).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("|table","").replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",qn).getRegex(),xm=O(/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/).replace("paragraph",br).getRegex(),Ks={blockquote:xm,code:mm,def:km,fences:bm,heading:ym,hr:Qt,html:Sm,lheading:mr,list:Am,newline:vm,paragraph:br,table:Dt,text:$m},yo=O("^ *([^\\n ].*)\\n {0,3}((?:\\| *)?:?-+:? *(?:\\| *:?-+:? *)*(?:\\| *)?)(?:\\n((?:(?! *\\n|hr|heading|blockquote|code|fences|list|html).*(?:\\n|$))*)\\n*|$)").replace("hr",Qt).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("blockquote"," {0,3}>").replace("code","(?: {4}| {0,3}	)[^\\n]").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",qn).getRegex(),_m={...Ks,lheading:wm,table:yo,paragraph:O(Ds).replace("hr",Qt).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("table",yo).replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",qn).getRegex()},Cm={...Ks,html:O(`^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:"[^"]*"|'[^']*'|\\s[^'"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))`).replace("comment",Us).replace(/tag/g,"(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/,heading:/^(#{1,6})(.*)(?:\n+|$)/,fences:Dt,lheading:/^(.+?)\n {0,3}(=+|-+) *(?:\n+|$)/,paragraph:O(Ds).replace("hr",Qt).replace("heading",` *#{1,6} *[^
]`).replace("lheading",mr).replace("|table","").replace("blockquote"," {0,3}>").replace("|fences","").replace("|list","").replace("|html","").replace("|tag","").getRegex()},Em=/^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/,Tm=/^(`+)([^`]|[^`][\s\S]*?[^`])\1(?!`)/,yr=/^( {2,}|\\)\n(?!\s*$)/,Lm=/^(`+|[^`])(?:(?= {2,}\n)|[\s\S]*?(?:(?=[\\<!\[`*_]|\b_|$)|[^ ](?= {2,}\n)))/,Vn=/[\p{P}\p{S}]/u,zs=/[\s\p{P}\p{S}]/u,wr=/[^\s\p{P}\p{S}]/u,Im=O(/^((?![*_])punctSpace)/,"u").replace(/punctSpace/g,zs).getRegex(),$r=/(?!~)[\p{P}\p{S}]/u,Rm=/(?!~)[\s\p{P}\p{S}]/u,Mm=/(?:[^\s\p{P}\p{S}]|~)/u,Pm=O(/link|precode-code|html/,"g").replace("link",/\[(?:[^\[\]`]|(?<a>`+)[^`]+\k<a>(?!`))*?\]\((?:\\[\s\S]|[^\\\(\)]|\((?:\\[\s\S]|[^\\\(\)])*\))*\)/).replace("precode-",pm?"(?<!`)()":"(^^|[^`])").replace("code",/(?<b>`+)[^`]+\k<b>(?!`)/).replace("html",/<(?! )[^<>]*?>/).getRegex(),kr=/^(?:\*+(?:((?!\*)punct)|[^\s*]))|^_+(?:((?!_)punct)|([^\s_]))/,Fm=O(kr,"u").replace(/punct/g,Vn).getRegex(),Nm=O(kr,"u").replace(/punct/g,$r).getRegex(),Ar="^[^_*]*?__[^_*]*?\\*[^_*]*?(?=__)|[^*]+(?=[^*])|(?!\\*)punct(\\*+)(?=[\\s]|$)|notPunctSpace(\\*+)(?!\\*)(?=punctSpace|$)|(?!\\*)punctSpace(\\*+)(?=notPunctSpace)|[\\s](\\*+)(?!\\*)(?=punct)|(?!\\*)punct(\\*+)(?!\\*)(?=punct)|notPunctSpace(\\*+)(?=notPunctSpace)",Om=O(Ar,"gu").replace(/notPunctSpace/g,wr).replace(/punctSpace/g,zs).replace(/punct/g,Vn).getRegex(),Dm=O(Ar,"gu").replace(/notPunctSpace/g,Mm).replace(/punctSpace/g,Rm).replace(/punct/g,$r).getRegex(),Bm=O("^[^_*]*?\\*\\*[^_*]*?_[^_*]*?(?=\\*\\*)|[^_]+(?=[^_])|(?!_)punct(_+)(?=[\\s]|$)|notPunctSpace(_+)(?!_)(?=punctSpace|$)|(?!_)punctSpace(_+)(?=notPunctSpace)|[\\s](_+)(?!_)(?=punct)|(?!_)punct(_+)(?!_)(?=punct)","gu").replace(/notPunctSpace/g,wr).replace(/punctSpace/g,zs).replace(/punct/g,Vn).getRegex(),Um=O(/\\(punct)/,"gu").replace(/punct/g,Vn).getRegex(),Km=O(/^<(scheme:[^\s\x00-\x1f<>]*|email)>/).replace("scheme",/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/).replace("email",/[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/).getRegex(),zm=O(Us).replace("(?:-->|$)","-->").getRegex(),Hm=O("^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>").replace("comment",zm).replace("attribute",/\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/).getRegex(),In=/(?:\[(?:\\[\s\S]|[^\[\]\\])*\]|\\[\s\S]|`+[^`]*?`+(?!`)|[^\[\]\\`])*?/,jm=O(/^!?\[(label)\]\(\s*(href)(?:(?:[ \t]*(?:\n[ \t]*)?)(title))?\s*\)/).replace("label",In).replace("href",/<(?:\\.|[^\n<>\\])+>|[^ \t\n\x00-\x1f]*/).replace("title",/"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/).getRegex(),Sr=O(/^!?\[(label)\]\[(ref)\]/).replace("label",In).replace("ref",Bs).getRegex(),xr=O(/^!?\[(ref)\](?:\[\])?/).replace("ref",Bs).getRegex(),Gm=O("reflink|nolink(?!\\()","g").replace("reflink",Sr).replace("nolink",xr).getRegex(),wo=/[hH][tT][tT][pP][sS]?|[fF][tT][pP]/,Hs={_backpedal:Dt,anyPunctuation:Um,autolink:Km,blockSkip:Pm,br:yr,code:Tm,del:Dt,emStrongLDelim:Fm,emStrongRDelimAst:Om,emStrongRDelimUnd:Bm,escape:Em,link:jm,nolink:xr,punctuation:Im,reflink:Sr,reflinkSearch:Gm,tag:Hm,text:Lm,url:Dt},Wm={...Hs,link:O(/^!?\[(label)\]\((.*?)\)/).replace("label",In).getRegex(),reflink:O(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label",In).getRegex()},es={...Hs,emStrongRDelimAst:Dm,emStrongLDelim:Nm,url:O(/^((?:protocol):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/).replace("protocol",wo).replace("email",/[A-Za-z0-9._+-]+(@)[a-zA-Z0-9-_]+(?:\.[a-zA-Z0-9-_]*[a-zA-Z0-9])+(?![-_])/).getRegex(),_backpedal:/(?:[^?!.,:;*_'"~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_'"~)]+(?!$))+/,del:/^(~~?)(?=[^\s~])((?:\\[\s\S]|[^\\])*?(?:\\[\s\S]|[^\s~\\]))\1(?=[^~]|$)/,text:O(/^([`~]+|[^`~])(?:(?= {2,}\n)|(?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)|[\s\S]*?(?:(?=[\\<!\[`*~_]|\b_|protocol:\/\/|www\.|$)|[^ ](?= {2,}\n)|[^a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-](?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)))/).replace("protocol",wo).getRegex()},qm={...es,br:O(yr).replace("{2,}","*").getRegex(),text:O(es.text).replace("\\b_","\\b_| {2,}\\n").replace(/\{2,\}/g,"*").getRegex()},pn={normal:Ks,gfm:_m,pedantic:Cm},Ct={normal:Hs,gfm:es,breaks:qm,pedantic:Wm},Vm={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"},$o=e=>Vm[e];function Te(e,t){if(t){if(ne.escapeTest.test(e))return e.replace(ne.escapeReplace,$o)}else if(ne.escapeTestNoEncode.test(e))return e.replace(ne.escapeReplaceNoEncode,$o);return e}function ko(e){try{e=encodeURI(e).replace(ne.percentDecode,"%")}catch{return null}return e}function Ao(e,t){let n=e.replace(ne.findPipe,(a,o,l)=>{let d=!1,h=o;for(;--h>=0&&l[h]==="\\";)d=!d;return d?"|":" |"}),i=n.split(ne.splitPipe),s=0;if(i[0].trim()||i.shift(),i.length>0&&!i.at(-1)?.trim()&&i.pop(),t)if(i.length>t)i.splice(t);else for(;i.length<t;)i.push("");for(;s<i.length;s++)i[s]=i[s].trim().replace(ne.slashPipe,"|");return i}function Et(e,t,n){let i=e.length;if(i===0)return"";let s=0;for(;s<i&&e.charAt(i-s-1)===t;)s++;return e.slice(0,i-s)}function Ym(e,t){if(e.indexOf(t[1])===-1)return-1;let n=0;for(let i=0;i<e.length;i++)if(e[i]==="\\")i++;else if(e[i]===t[0])n++;else if(e[i]===t[1]&&(n--,n<0))return i;return n>0?-2:-1}function So(e,t,n,i,s){let a=t.href,o=t.title||null,l=e[1].replace(s.other.outputLinkReplace,"$1");i.state.inLink=!0;let d={type:e[0].charAt(0)==="!"?"image":"link",raw:n,href:a,title:o,text:l,tokens:i.inlineTokens(l)};return i.state.inLink=!1,d}function Qm(e,t,n){let i=e.match(n.other.indentCodeCompensation);if(i===null)return t;let s=i[1];return t.split(`
`).map(a=>{let o=a.match(n.other.beginningSpace);if(o===null)return a;let[l]=o;return l.length>=s.length?a.slice(s.length):a}).join(`
`)}var Rn=class{options;rules;lexer;constructor(e){this.options=e||it}space(e){let t=this.rules.block.newline.exec(e);if(t&&t[0].length>0)return{type:"space",raw:t[0]}}code(e){let t=this.rules.block.code.exec(e);if(t){let n=t[0].replace(this.rules.other.codeRemoveIndent,"");return{type:"code",raw:t[0],codeBlockStyle:"indented",text:this.options.pedantic?n:Et(n,`
`)}}}fences(e){let t=this.rules.block.fences.exec(e);if(t){let n=t[0],i=Qm(n,t[3]||"",this.rules);return{type:"code",raw:n,lang:t[2]?t[2].trim().replace(this.rules.inline.anyPunctuation,"$1"):t[2],text:i}}}heading(e){let t=this.rules.block.heading.exec(e);if(t){let n=t[2].trim();if(this.rules.other.endingHash.test(n)){let i=Et(n,"#");(this.options.pedantic||!i||this.rules.other.endingSpaceChar.test(i))&&(n=i.trim())}return{type:"heading",raw:t[0],depth:t[1].length,text:n,tokens:this.lexer.inline(n)}}}hr(e){let t=this.rules.block.hr.exec(e);if(t)return{type:"hr",raw:Et(t[0],`
`)}}blockquote(e){let t=this.rules.block.blockquote.exec(e);if(t){let n=Et(t[0],`
`).split(`
`),i="",s="",a=[];for(;n.length>0;){let o=!1,l=[],d;for(d=0;d<n.length;d++)if(this.rules.other.blockquoteStart.test(n[d]))l.push(n[d]),o=!0;else if(!o)l.push(n[d]);else break;n=n.slice(d);let h=l.join(`
`),p=h.replace(this.rules.other.blockquoteSetextReplace,`
    $1`).replace(this.rules.other.blockquoteSetextReplace2,"");i=i?`${i}
${h}`:h,s=s?`${s}
${p}`:p;let u=this.lexer.state.top;if(this.lexer.state.top=!0,this.lexer.blockTokens(p,a,!0),this.lexer.state.top=u,n.length===0)break;let y=a.at(-1);if(y?.type==="code")break;if(y?.type==="blockquote"){let v=y,$=v.raw+`
`+n.join(`
`),g=this.blockquote($);a[a.length-1]=g,i=i.substring(0,i.length-v.raw.length)+g.raw,s=s.substring(0,s.length-v.text.length)+g.text;break}else if(y?.type==="list"){let v=y,$=v.raw+`
`+n.join(`
`),g=this.list($);a[a.length-1]=g,i=i.substring(0,i.length-y.raw.length)+g.raw,s=s.substring(0,s.length-v.raw.length)+g.raw,n=$.substring(a.at(-1).raw.length).split(`
`);continue}}return{type:"blockquote",raw:i,tokens:a,text:s}}}list(e){let t=this.rules.block.list.exec(e);if(t){let n=t[1].trim(),i=n.length>1,s={type:"list",raw:"",ordered:i,start:i?+n.slice(0,-1):"",loose:!1,items:[]};n=i?`\\d{1,9}\\${n.slice(-1)}`:`\\${n}`,this.options.pedantic&&(n=i?n:"[*+-]");let a=this.rules.other.listItemRegex(n),o=!1;for(;e;){let d=!1,h="",p="";if(!(t=a.exec(e))||this.rules.block.hr.test(e))break;h=t[0],e=e.substring(h.length);let u=t[2].split(`
`,1)[0].replace(this.rules.other.listReplaceTabs,g=>" ".repeat(3*g.length)),y=e.split(`
`,1)[0],v=!u.trim(),$=0;if(this.options.pedantic?($=2,p=u.trimStart()):v?$=t[1].length+1:($=t[2].search(this.rules.other.nonSpaceChar),$=$>4?1:$,p=u.slice($),$+=t[1].length),v&&this.rules.other.blankLine.test(y)&&(h+=y+`
`,e=e.substring(y.length+1),d=!0),!d){let g=this.rules.other.nextBulletRegex($),w=this.rules.other.hrRegex($),_=this.rules.other.fencesBeginRegex($),C=this.rules.other.headingBeginRegex($),L=this.rules.other.htmlBeginRegex($);for(;e;){let x=e.split(`
`,1)[0],T;if(y=x,this.options.pedantic?(y=y.replace(this.rules.other.listReplaceNesting,"  "),T=y):T=y.replace(this.rules.other.tabCharGlobal,"    "),_.test(y)||C.test(y)||L.test(y)||g.test(y)||w.test(y))break;if(T.search(this.rules.other.nonSpaceChar)>=$||!y.trim())p+=`
`+T.slice($);else{if(v||u.replace(this.rules.other.tabCharGlobal,"    ").search(this.rules.other.nonSpaceChar)>=4||_.test(u)||C.test(u)||w.test(u))break;p+=`
`+y}!v&&!y.trim()&&(v=!0),h+=x+`
`,e=e.substring(x.length+1),u=T.slice($)}}s.loose||(o?s.loose=!0:this.rules.other.doubleBlankLine.test(h)&&(o=!0)),s.items.push({type:"list_item",raw:h,task:!!this.options.gfm&&this.rules.other.listIsTask.test(p),loose:!1,text:p,tokens:[]}),s.raw+=h}let l=s.items.at(-1);if(l)l.raw=l.raw.trimEnd(),l.text=l.text.trimEnd();else return;s.raw=s.raw.trimEnd();for(let d of s.items){if(this.lexer.state.top=!1,d.tokens=this.lexer.blockTokens(d.text,[]),d.task){if(d.text=d.text.replace(this.rules.other.listReplaceTask,""),d.tokens[0]?.type==="text"||d.tokens[0]?.type==="paragraph"){d.tokens[0].raw=d.tokens[0].raw.replace(this.rules.other.listReplaceTask,""),d.tokens[0].text=d.tokens[0].text.replace(this.rules.other.listReplaceTask,"");for(let p=this.lexer.inlineQueue.length-1;p>=0;p--)if(this.rules.other.listIsTask.test(this.lexer.inlineQueue[p].src)){this.lexer.inlineQueue[p].src=this.lexer.inlineQueue[p].src.replace(this.rules.other.listReplaceTask,"");break}}let h=this.rules.other.listTaskCheckbox.exec(d.raw);if(h){let p={type:"checkbox",raw:h[0]+" ",checked:h[0]!=="[ ]"};d.checked=p.checked,s.loose?d.tokens[0]&&["paragraph","text"].includes(d.tokens[0].type)&&"tokens"in d.tokens[0]&&d.tokens[0].tokens?(d.tokens[0].raw=p.raw+d.tokens[0].raw,d.tokens[0].text=p.raw+d.tokens[0].text,d.tokens[0].tokens.unshift(p)):d.tokens.unshift({type:"paragraph",raw:p.raw,text:p.raw,tokens:[p]}):d.tokens.unshift(p)}}if(!s.loose){let h=d.tokens.filter(u=>u.type==="space"),p=h.length>0&&h.some(u=>this.rules.other.anyLine.test(u.raw));s.loose=p}}if(s.loose)for(let d of s.items){d.loose=!0;for(let h of d.tokens)h.type==="text"&&(h.type="paragraph")}return s}}html(e){let t=this.rules.block.html.exec(e);if(t)return{type:"html",block:!0,raw:t[0],pre:t[1]==="pre"||t[1]==="script"||t[1]==="style",text:t[0]}}def(e){let t=this.rules.block.def.exec(e);if(t){let n=t[1].toLowerCase().replace(this.rules.other.multipleSpaceGlobal," "),i=t[2]?t[2].replace(this.rules.other.hrefBrackets,"$1").replace(this.rules.inline.anyPunctuation,"$1"):"",s=t[3]?t[3].substring(1,t[3].length-1).replace(this.rules.inline.anyPunctuation,"$1"):t[3];return{type:"def",tag:n,raw:t[0],href:i,title:s}}}table(e){let t=this.rules.block.table.exec(e);if(!t||!this.rules.other.tableDelimiter.test(t[2]))return;let n=Ao(t[1]),i=t[2].replace(this.rules.other.tableAlignChars,"").split("|"),s=t[3]?.trim()?t[3].replace(this.rules.other.tableRowBlankLine,"").split(`
`):[],a={type:"table",raw:t[0],header:[],align:[],rows:[]};if(n.length===i.length){for(let o of i)this.rules.other.tableAlignRight.test(o)?a.align.push("right"):this.rules.other.tableAlignCenter.test(o)?a.align.push("center"):this.rules.other.tableAlignLeft.test(o)?a.align.push("left"):a.align.push(null);for(let o=0;o<n.length;o++)a.header.push({text:n[o],tokens:this.lexer.inline(n[o]),header:!0,align:a.align[o]});for(let o of s)a.rows.push(Ao(o,a.header.length).map((l,d)=>({text:l,tokens:this.lexer.inline(l),header:!1,align:a.align[d]})));return a}}lheading(e){let t=this.rules.block.lheading.exec(e);if(t)return{type:"heading",raw:t[0],depth:t[2].charAt(0)==="="?1:2,text:t[1],tokens:this.lexer.inline(t[1])}}paragraph(e){let t=this.rules.block.paragraph.exec(e);if(t){let n=t[1].charAt(t[1].length-1)===`
`?t[1].slice(0,-1):t[1];return{type:"paragraph",raw:t[0],text:n,tokens:this.lexer.inline(n)}}}text(e){let t=this.rules.block.text.exec(e);if(t)return{type:"text",raw:t[0],text:t[0],tokens:this.lexer.inline(t[0])}}escape(e){let t=this.rules.inline.escape.exec(e);if(t)return{type:"escape",raw:t[0],text:t[1]}}tag(e){let t=this.rules.inline.tag.exec(e);if(t)return!this.lexer.state.inLink&&this.rules.other.startATag.test(t[0])?this.lexer.state.inLink=!0:this.lexer.state.inLink&&this.rules.other.endATag.test(t[0])&&(this.lexer.state.inLink=!1),!this.lexer.state.inRawBlock&&this.rules.other.startPreScriptTag.test(t[0])?this.lexer.state.inRawBlock=!0:this.lexer.state.inRawBlock&&this.rules.other.endPreScriptTag.test(t[0])&&(this.lexer.state.inRawBlock=!1),{type:"html",raw:t[0],inLink:this.lexer.state.inLink,inRawBlock:this.lexer.state.inRawBlock,block:!1,text:t[0]}}link(e){let t=this.rules.inline.link.exec(e);if(t){let n=t[2].trim();if(!this.options.pedantic&&this.rules.other.startAngleBracket.test(n)){if(!this.rules.other.endAngleBracket.test(n))return;let a=Et(n.slice(0,-1),"\\");if((n.length-a.length)%2===0)return}else{let a=Ym(t[2],"()");if(a===-2)return;if(a>-1){let o=(t[0].indexOf("!")===0?5:4)+t[1].length+a;t[2]=t[2].substring(0,a),t[0]=t[0].substring(0,o).trim(),t[3]=""}}let i=t[2],s="";if(this.options.pedantic){let a=this.rules.other.pedanticHrefTitle.exec(i);a&&(i=a[1],s=a[3])}else s=t[3]?t[3].slice(1,-1):"";return i=i.trim(),this.rules.other.startAngleBracket.test(i)&&(this.options.pedantic&&!this.rules.other.endAngleBracket.test(n)?i=i.slice(1):i=i.slice(1,-1)),So(t,{href:i&&i.replace(this.rules.inline.anyPunctuation,"$1"),title:s&&s.replace(this.rules.inline.anyPunctuation,"$1")},t[0],this.lexer,this.rules)}}reflink(e,t){let n;if((n=this.rules.inline.reflink.exec(e))||(n=this.rules.inline.nolink.exec(e))){let i=(n[2]||n[1]).replace(this.rules.other.multipleSpaceGlobal," "),s=t[i.toLowerCase()];if(!s){let a=n[0].charAt(0);return{type:"text",raw:a,text:a}}return So(n,s,n[0],this.lexer,this.rules)}}emStrong(e,t,n=""){let i=this.rules.inline.emStrongLDelim.exec(e);if(!(!i||i[3]&&n.match(this.rules.other.unicodeAlphaNumeric))&&(!(i[1]||i[2])||!n||this.rules.inline.punctuation.exec(n))){let s=[...i[0]].length-1,a,o,l=s,d=0,h=i[0][0]==="*"?this.rules.inline.emStrongRDelimAst:this.rules.inline.emStrongRDelimUnd;for(h.lastIndex=0,t=t.slice(-1*e.length+s);(i=h.exec(t))!=null;){if(a=i[1]||i[2]||i[3]||i[4]||i[5]||i[6],!a)continue;if(o=[...a].length,i[3]||i[4]){l+=o;continue}else if((i[5]||i[6])&&s%3&&!((s+o)%3)){d+=o;continue}if(l-=o,l>0)continue;o=Math.min(o,o+l+d);let p=[...i[0]][0].length,u=e.slice(0,s+i.index+p+o);if(Math.min(s,o)%2){let v=u.slice(1,-1);return{type:"em",raw:u,text:v,tokens:this.lexer.inlineTokens(v)}}let y=u.slice(2,-2);return{type:"strong",raw:u,text:y,tokens:this.lexer.inlineTokens(y)}}}}codespan(e){let t=this.rules.inline.code.exec(e);if(t){let n=t[2].replace(this.rules.other.newLineCharGlobal," "),i=this.rules.other.nonSpaceChar.test(n),s=this.rules.other.startingSpaceChar.test(n)&&this.rules.other.endingSpaceChar.test(n);return i&&s&&(n=n.substring(1,n.length-1)),{type:"codespan",raw:t[0],text:n}}}br(e){let t=this.rules.inline.br.exec(e);if(t)return{type:"br",raw:t[0]}}del(e){let t=this.rules.inline.del.exec(e);if(t)return{type:"del",raw:t[0],text:t[2],tokens:this.lexer.inlineTokens(t[2])}}autolink(e){let t=this.rules.inline.autolink.exec(e);if(t){let n,i;return t[2]==="@"?(n=t[1],i="mailto:"+n):(n=t[1],i=n),{type:"link",raw:t[0],text:n,href:i,tokens:[{type:"text",raw:n,text:n}]}}}url(e){let t;if(t=this.rules.inline.url.exec(e)){let n,i;if(t[2]==="@")n=t[0],i="mailto:"+n;else{let s;do s=t[0],t[0]=this.rules.inline._backpedal.exec(t[0])?.[0]??"";while(s!==t[0]);n=t[0],t[1]==="www."?i="http://"+t[0]:i=t[0]}return{type:"link",raw:t[0],text:n,href:i,tokens:[{type:"text",raw:n,text:n}]}}}inlineText(e){let t=this.rules.inline.text.exec(e);if(t){let n=this.lexer.state.inRawBlock;return{type:"text",raw:t[0],text:t[0],escaped:n}}}},pe=class ts{tokens;options;state;inlineQueue;tokenizer;constructor(t){this.tokens=[],this.tokens.links=Object.create(null),this.options=t||it,this.options.tokenizer=this.options.tokenizer||new Rn,this.tokenizer=this.options.tokenizer,this.tokenizer.options=this.options,this.tokenizer.lexer=this,this.inlineQueue=[],this.state={inLink:!1,inRawBlock:!1,top:!0};let n={other:ne,block:pn.normal,inline:Ct.normal};this.options.pedantic?(n.block=pn.pedantic,n.inline=Ct.pedantic):this.options.gfm&&(n.block=pn.gfm,this.options.breaks?n.inline=Ct.breaks:n.inline=Ct.gfm),this.tokenizer.rules=n}static get rules(){return{block:pn,inline:Ct}}static lex(t,n){return new ts(n).lex(t)}static lexInline(t,n){return new ts(n).inlineTokens(t)}lex(t){t=t.replace(ne.carriageReturn,`
`),this.blockTokens(t,this.tokens);for(let n=0;n<this.inlineQueue.length;n++){let i=this.inlineQueue[n];this.inlineTokens(i.src,i.tokens)}return this.inlineQueue=[],this.tokens}blockTokens(t,n=[],i=!1){for(this.options.pedantic&&(t=t.replace(ne.tabCharGlobal,"    ").replace(ne.spaceLine,""));t;){let s;if(this.options.extensions?.block?.some(o=>(s=o.call({lexer:this},t,n))?(t=t.substring(s.raw.length),n.push(s),!0):!1))continue;if(s=this.tokenizer.space(t)){t=t.substring(s.raw.length);let o=n.at(-1);s.raw.length===1&&o!==void 0?o.raw+=`
`:n.push(s);continue}if(s=this.tokenizer.code(t)){t=t.substring(s.raw.length);let o=n.at(-1);o?.type==="paragraph"||o?.type==="text"?(o.raw+=(o.raw.endsWith(`
`)?"":`
`)+s.raw,o.text+=`
`+s.text,this.inlineQueue.at(-1).src=o.text):n.push(s);continue}if(s=this.tokenizer.fences(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.heading(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.hr(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.blockquote(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.list(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.html(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.def(t)){t=t.substring(s.raw.length);let o=n.at(-1);o?.type==="paragraph"||o?.type==="text"?(o.raw+=(o.raw.endsWith(`
`)?"":`
`)+s.raw,o.text+=`
`+s.raw,this.inlineQueue.at(-1).src=o.text):this.tokens.links[s.tag]||(this.tokens.links[s.tag]={href:s.href,title:s.title},n.push(s));continue}if(s=this.tokenizer.table(t)){t=t.substring(s.raw.length),n.push(s);continue}if(s=this.tokenizer.lheading(t)){t=t.substring(s.raw.length),n.push(s);continue}let a=t;if(this.options.extensions?.startBlock){let o=1/0,l=t.slice(1),d;this.options.extensions.startBlock.forEach(h=>{d=h.call({lexer:this},l),typeof d=="number"&&d>=0&&(o=Math.min(o,d))}),o<1/0&&o>=0&&(a=t.substring(0,o+1))}if(this.state.top&&(s=this.tokenizer.paragraph(a))){let o=n.at(-1);i&&o?.type==="paragraph"?(o.raw+=(o.raw.endsWith(`
`)?"":`
`)+s.raw,o.text+=`
`+s.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=o.text):n.push(s),i=a.length!==t.length,t=t.substring(s.raw.length);continue}if(s=this.tokenizer.text(t)){t=t.substring(s.raw.length);let o=n.at(-1);o?.type==="text"?(o.raw+=(o.raw.endsWith(`
`)?"":`
`)+s.raw,o.text+=`
`+s.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=o.text):n.push(s);continue}if(t){let o="Infinite loop on byte: "+t.charCodeAt(0);if(this.options.silent){console.error(o);break}else throw new Error(o)}}return this.state.top=!0,n}inline(t,n=[]){return this.inlineQueue.push({src:t,tokens:n}),n}inlineTokens(t,n=[]){let i=t,s=null;if(this.tokens.links){let d=Object.keys(this.tokens.links);if(d.length>0)for(;(s=this.tokenizer.rules.inline.reflinkSearch.exec(i))!=null;)d.includes(s[0].slice(s[0].lastIndexOf("[")+1,-1))&&(i=i.slice(0,s.index)+"["+"a".repeat(s[0].length-2)+"]"+i.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex))}for(;(s=this.tokenizer.rules.inline.anyPunctuation.exec(i))!=null;)i=i.slice(0,s.index)+"++"+i.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);let a;for(;(s=this.tokenizer.rules.inline.blockSkip.exec(i))!=null;)a=s[2]?s[2].length:0,i=i.slice(0,s.index+a)+"["+"a".repeat(s[0].length-a-2)+"]"+i.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);i=this.options.hooks?.emStrongMask?.call({lexer:this},i)??i;let o=!1,l="";for(;t;){o||(l=""),o=!1;let d;if(this.options.extensions?.inline?.some(p=>(d=p.call({lexer:this},t,n))?(t=t.substring(d.raw.length),n.push(d),!0):!1))continue;if(d=this.tokenizer.escape(t)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.tag(t)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.link(t)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.reflink(t,this.tokens.links)){t=t.substring(d.raw.length);let p=n.at(-1);d.type==="text"&&p?.type==="text"?(p.raw+=d.raw,p.text+=d.text):n.push(d);continue}if(d=this.tokenizer.emStrong(t,i,l)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.codespan(t)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.br(t)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.del(t)){t=t.substring(d.raw.length),n.push(d);continue}if(d=this.tokenizer.autolink(t)){t=t.substring(d.raw.length),n.push(d);continue}if(!this.state.inLink&&(d=this.tokenizer.url(t))){t=t.substring(d.raw.length),n.push(d);continue}let h=t;if(this.options.extensions?.startInline){let p=1/0,u=t.slice(1),y;this.options.extensions.startInline.forEach(v=>{y=v.call({lexer:this},u),typeof y=="number"&&y>=0&&(p=Math.min(p,y))}),p<1/0&&p>=0&&(h=t.substring(0,p+1))}if(d=this.tokenizer.inlineText(h)){t=t.substring(d.raw.length),d.raw.slice(-1)!=="_"&&(l=d.raw.slice(-1)),o=!0;let p=n.at(-1);p?.type==="text"?(p.raw+=d.raw,p.text+=d.text):n.push(d);continue}if(t){let p="Infinite loop on byte: "+t.charCodeAt(0);if(this.options.silent){console.error(p);break}else throw new Error(p)}}return n}},Mn=class{options;parser;constructor(e){this.options=e||it}space(e){return""}code({text:e,lang:t,escaped:n}){let i=(t||"").match(ne.notSpaceStart)?.[0],s=e.replace(ne.endingNewline,"")+`
`;return i?'<pre><code class="language-'+Te(i)+'">'+(n?s:Te(s,!0))+`</code></pre>
`:"<pre><code>"+(n?s:Te(s,!0))+`</code></pre>
`}blockquote({tokens:e}){return`<blockquote>
${this.parser.parse(e)}</blockquote>
`}html({text:e}){return e}def(e){return""}heading({tokens:e,depth:t}){return`<h${t}>${this.parser.parseInline(e)}</h${t}>
`}hr(e){return`<hr>
`}list(e){let t=e.ordered,n=e.start,i="";for(let o=0;o<e.items.length;o++){let l=e.items[o];i+=this.listitem(l)}let s=t?"ol":"ul",a=t&&n!==1?' start="'+n+'"':"";return"<"+s+a+`>
`+i+"</"+s+`>
`}listitem(e){return`<li>${this.parser.parse(e.tokens)}</li>
`}checkbox({checked:e}){return"<input "+(e?'checked="" ':"")+'disabled="" type="checkbox"> '}paragraph({tokens:e}){return`<p>${this.parser.parseInline(e)}</p>
`}table(e){let t="",n="";for(let s=0;s<e.header.length;s++)n+=this.tablecell(e.header[s]);t+=this.tablerow({text:n});let i="";for(let s=0;s<e.rows.length;s++){let a=e.rows[s];n="";for(let o=0;o<a.length;o++)n+=this.tablecell(a[o]);i+=this.tablerow({text:n})}return i&&(i=`<tbody>${i}</tbody>`),`<table>
<thead>
`+t+`</thead>
`+i+`</table>
`}tablerow({text:e}){return`<tr>
${e}</tr>
`}tablecell(e){let t=this.parser.parseInline(e.tokens),n=e.header?"th":"td";return(e.align?`<${n} align="${e.align}">`:`<${n}>`)+t+`</${n}>
`}strong({tokens:e}){return`<strong>${this.parser.parseInline(e)}</strong>`}em({tokens:e}){return`<em>${this.parser.parseInline(e)}</em>`}codespan({text:e}){return`<code>${Te(e,!0)}</code>`}br(e){return"<br>"}del({tokens:e}){return`<del>${this.parser.parseInline(e)}</del>`}link({href:e,title:t,tokens:n}){let i=this.parser.parseInline(n),s=ko(e);if(s===null)return i;e=s;let a='<a href="'+e+'"';return t&&(a+=' title="'+Te(t)+'"'),a+=">"+i+"</a>",a}image({href:e,title:t,text:n,tokens:i}){i&&(n=this.parser.parseInline(i,this.parser.textRenderer));let s=ko(e);if(s===null)return Te(n);e=s;let a=`<img src="${e}" alt="${n}"`;return t&&(a+=` title="${Te(t)}"`),a+=">",a}text(e){return"tokens"in e&&e.tokens?this.parser.parseInline(e.tokens):"escaped"in e&&e.escaped?e.text:Te(e.text)}},js=class{strong({text:e}){return e}em({text:e}){return e}codespan({text:e}){return e}del({text:e}){return e}html({text:e}){return e}text({text:e}){return e}link({text:e}){return""+e}image({text:e}){return""+e}br(){return""}checkbox({raw:e}){return e}},ve=class ns{options;renderer;textRenderer;constructor(t){this.options=t||it,this.options.renderer=this.options.renderer||new Mn,this.renderer=this.options.renderer,this.renderer.options=this.options,this.renderer.parser=this,this.textRenderer=new js}static parse(t,n){return new ns(n).parse(t)}static parseInline(t,n){return new ns(n).parseInline(t)}parse(t){let n="";for(let i=0;i<t.length;i++){let s=t[i];if(this.options.extensions?.renderers?.[s.type]){let o=s,l=this.options.extensions.renderers[o.type].call({parser:this},o);if(l!==!1||!["space","hr","heading","code","table","blockquote","list","html","def","paragraph","text"].includes(o.type)){n+=l||"";continue}}let a=s;switch(a.type){case"space":{n+=this.renderer.space(a);break}case"hr":{n+=this.renderer.hr(a);break}case"heading":{n+=this.renderer.heading(a);break}case"code":{n+=this.renderer.code(a);break}case"table":{n+=this.renderer.table(a);break}case"blockquote":{n+=this.renderer.blockquote(a);break}case"list":{n+=this.renderer.list(a);break}case"checkbox":{n+=this.renderer.checkbox(a);break}case"html":{n+=this.renderer.html(a);break}case"def":{n+=this.renderer.def(a);break}case"paragraph":{n+=this.renderer.paragraph(a);break}case"text":{n+=this.renderer.text(a);break}default:{let o='Token with "'+a.type+'" type was not found.';if(this.options.silent)return console.error(o),"";throw new Error(o)}}}return n}parseInline(t,n=this.renderer){let i="";for(let s=0;s<t.length;s++){let a=t[s];if(this.options.extensions?.renderers?.[a.type]){let l=this.options.extensions.renderers[a.type].call({parser:this},a);if(l!==!1||!["escape","html","link","image","strong","em","codespan","br","del","text"].includes(a.type)){i+=l||"";continue}}let o=a;switch(o.type){case"escape":{i+=n.text(o);break}case"html":{i+=n.html(o);break}case"link":{i+=n.link(o);break}case"image":{i+=n.image(o);break}case"checkbox":{i+=n.checkbox(o);break}case"strong":{i+=n.strong(o);break}case"em":{i+=n.em(o);break}case"codespan":{i+=n.codespan(o);break}case"br":{i+=n.br(o);break}case"del":{i+=n.del(o);break}case"text":{i+=n.text(o);break}default:{let l='Token with "'+o.type+'" type was not found.';if(this.options.silent)return console.error(l),"";throw new Error(l)}}}return i}},Lt=class{options;block;constructor(e){this.options=e||it}static passThroughHooks=new Set(["preprocess","postprocess","processAllTokens","emStrongMask"]);static passThroughHooksRespectAsync=new Set(["preprocess","postprocess","processAllTokens"]);preprocess(e){return e}postprocess(e){return e}processAllTokens(e){return e}emStrongMask(e){return e}provideLexer(){return this.block?pe.lex:pe.lexInline}provideParser(){return this.block?ve.parse:ve.parseInline}},Jm=class{defaults=Ns();options=this.setOptions;parse=this.parseMarkdown(!0);parseInline=this.parseMarkdown(!1);Parser=ve;Renderer=Mn;TextRenderer=js;Lexer=pe;Tokenizer=Rn;Hooks=Lt;constructor(...e){this.use(...e)}walkTokens(e,t){let n=[];for(let i of e)switch(n=n.concat(t.call(this,i)),i.type){case"table":{let s=i;for(let a of s.header)n=n.concat(this.walkTokens(a.tokens,t));for(let a of s.rows)for(let o of a)n=n.concat(this.walkTokens(o.tokens,t));break}case"list":{let s=i;n=n.concat(this.walkTokens(s.items,t));break}default:{let s=i;this.defaults.extensions?.childTokens?.[s.type]?this.defaults.extensions.childTokens[s.type].forEach(a=>{let o=s[a].flat(1/0);n=n.concat(this.walkTokens(o,t))}):s.tokens&&(n=n.concat(this.walkTokens(s.tokens,t)))}}return n}use(...e){let t=this.defaults.extensions||{renderers:{},childTokens:{}};return e.forEach(n=>{let i={...n};if(i.async=this.defaults.async||i.async||!1,n.extensions&&(n.extensions.forEach(s=>{if(!s.name)throw new Error("extension name required");if("renderer"in s){let a=t.renderers[s.name];a?t.renderers[s.name]=function(...o){let l=s.renderer.apply(this,o);return l===!1&&(l=a.apply(this,o)),l}:t.renderers[s.name]=s.renderer}if("tokenizer"in s){if(!s.level||s.level!=="block"&&s.level!=="inline")throw new Error("extension level must be 'block' or 'inline'");let a=t[s.level];a?a.unshift(s.tokenizer):t[s.level]=[s.tokenizer],s.start&&(s.level==="block"?t.startBlock?t.startBlock.push(s.start):t.startBlock=[s.start]:s.level==="inline"&&(t.startInline?t.startInline.push(s.start):t.startInline=[s.start]))}"childTokens"in s&&s.childTokens&&(t.childTokens[s.name]=s.childTokens)}),i.extensions=t),n.renderer){let s=this.defaults.renderer||new Mn(this.defaults);for(let a in n.renderer){if(!(a in s))throw new Error(`renderer '${a}' does not exist`);if(["options","parser"].includes(a))continue;let o=a,l=n.renderer[o],d=s[o];s[o]=(...h)=>{let p=l.apply(s,h);return p===!1&&(p=d.apply(s,h)),p||""}}i.renderer=s}if(n.tokenizer){let s=this.defaults.tokenizer||new Rn(this.defaults);for(let a in n.tokenizer){if(!(a in s))throw new Error(`tokenizer '${a}' does not exist`);if(["options","rules","lexer"].includes(a))continue;let o=a,l=n.tokenizer[o],d=s[o];s[o]=(...h)=>{let p=l.apply(s,h);return p===!1&&(p=d.apply(s,h)),p}}i.tokenizer=s}if(n.hooks){let s=this.defaults.hooks||new Lt;for(let a in n.hooks){if(!(a in s))throw new Error(`hook '${a}' does not exist`);if(["options","block"].includes(a))continue;let o=a,l=n.hooks[o],d=s[o];Lt.passThroughHooks.has(a)?s[o]=h=>{if(this.defaults.async&&Lt.passThroughHooksRespectAsync.has(a))return(async()=>{let u=await l.call(s,h);return d.call(s,u)})();let p=l.call(s,h);return d.call(s,p)}:s[o]=(...h)=>{if(this.defaults.async)return(async()=>{let u=await l.apply(s,h);return u===!1&&(u=await d.apply(s,h)),u})();let p=l.apply(s,h);return p===!1&&(p=d.apply(s,h)),p}}i.hooks=s}if(n.walkTokens){let s=this.defaults.walkTokens,a=n.walkTokens;i.walkTokens=function(o){let l=[];return l.push(a.call(this,o)),s&&(l=l.concat(s.call(this,o))),l}}this.defaults={...this.defaults,...i}}),this}setOptions(e){return this.defaults={...this.defaults,...e},this}lexer(e,t){return pe.lex(e,t??this.defaults)}parser(e,t){return ve.parse(e,t??this.defaults)}parseMarkdown(e){return(t,n)=>{let i={...n},s={...this.defaults,...i},a=this.onError(!!s.silent,!!s.async);if(this.defaults.async===!0&&i.async===!1)return a(new Error("marked(): The async option was set to true by an extension. Remove async: false from the parse options object to return a Promise."));if(typeof t>"u"||t===null)return a(new Error("marked(): input parameter is undefined or null"));if(typeof t!="string")return a(new Error("marked(): input parameter is of type "+Object.prototype.toString.call(t)+", string expected"));if(s.hooks&&(s.hooks.options=s,s.hooks.block=e),s.async)return(async()=>{let o=s.hooks?await s.hooks.preprocess(t):t,l=await(s.hooks?await s.hooks.provideLexer():e?pe.lex:pe.lexInline)(o,s),d=s.hooks?await s.hooks.processAllTokens(l):l;s.walkTokens&&await Promise.all(this.walkTokens(d,s.walkTokens));let h=await(s.hooks?await s.hooks.provideParser():e?ve.parse:ve.parseInline)(d,s);return s.hooks?await s.hooks.postprocess(h):h})().catch(a);try{s.hooks&&(t=s.hooks.preprocess(t));let o=(s.hooks?s.hooks.provideLexer():e?pe.lex:pe.lexInline)(t,s);s.hooks&&(o=s.hooks.processAllTokens(o)),s.walkTokens&&this.walkTokens(o,s.walkTokens);let l=(s.hooks?s.hooks.provideParser():e?ve.parse:ve.parseInline)(o,s);return s.hooks&&(l=s.hooks.postprocess(l)),l}catch(o){return a(o)}}}onError(e,t){return n=>{if(n.message+=`
Please report this to https://github.com/markedjs/marked.`,e){let i="<p>An error occurred:</p><pre>"+Te(n.message+"",!0)+"</pre>";return t?Promise.resolve(i):i}if(t)return Promise.reject(n);throw n}}},et=new Jm;function D(e,t){return et.parse(e,t)}D.options=D.setOptions=function(e){return et.setOptions(e),D.defaults=et.defaults,pr(D.defaults),D};D.getDefaults=Ns;D.defaults=it;D.use=function(...e){return et.use(...e),D.defaults=et.defaults,pr(D.defaults),D};D.walkTokens=function(e,t){return et.walkTokens(e,t)};D.parseInline=et.parseInline;D.Parser=ve;D.parser=ve.parse;D.Renderer=Mn;D.TextRenderer=js;D.Lexer=pe;D.lexer=pe.lex;D.Tokenizer=Rn;D.Hooks=Lt;D.parse=D;D.options;D.setOptions;D.use;D.walkTokens;D.parseInline;ve.parse;pe.lex;D.setOptions({gfm:!0,breaks:!0});const xo=["a","b","blockquote","br","code","del","em","h1","h2","h3","h4","hr","i","li","ol","p","pre","strong","table","tbody","td","th","thead","tr","ul"],_o=["class","href","rel","target","title","start"];let Co=!1;const Zm=14e4,Xm=4e4,eb=200,Ti=5e4,Ye=new Map;function tb(e){const t=Ye.get(e);return t===void 0?null:(Ye.delete(e),Ye.set(e,t),t)}function Eo(e,t){if(Ye.set(e,t),Ye.size<=eb)return;const n=Ye.keys().next().value;n&&Ye.delete(n)}function nb(){Co||(Co=!0,Xi.addHook("afterSanitizeAttributes",e=>{!(e instanceof HTMLAnchorElement)||!e.getAttribute("href")||(e.setAttribute("rel","noreferrer noopener"),e.setAttribute("target","_blank"))}))}function is(e){const t=e.trim();if(!t)return"";if(nb(),t.length<=Ti){const o=tb(t);if(o!==null)return o}const n=fl(t,Zm),i=n.truncated?`

… truncated (${n.total} chars, showing first ${n.text.length}).`:"";if(n.text.length>Xm){const l=`<pre class="code-block">${ib(`${n.text}${i}`)}</pre>`,d=Xi.sanitize(l,{ALLOWED_TAGS:xo,ALLOWED_ATTR:_o});return t.length<=Ti&&Eo(t,d),d}const s=D.parse(`${n.text}${i}`),a=Xi.sanitize(s,{ALLOWED_TAGS:xo,ALLOWED_ATTR:_o});return t.length<=Ti&&Eo(t,a),a}function ib(e){return e.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;")}const sb=1500,ab=2e3,_r="Copy as markdown",ob="Copied",lb="Copy failed";async function rb(e){if(!e)return!1;try{return await navigator.clipboard.writeText(e),!0}catch{return!1}}function vn(e,t){e.title=t,e.setAttribute("aria-label",t)}function cb(e){const t=e.label??_r;return r`
    <button
      class="chat-copy-btn"
      type="button"
      title=${t}
      aria-label=${t}
      @click=${async n=>{const i=n.currentTarget;if(!i||i.dataset.copying==="1")return;i.dataset.copying="1",i.setAttribute("aria-busy","true"),i.disabled=!0;const s=await rb(e.text());if(i.isConnected){if(delete i.dataset.copying,i.removeAttribute("aria-busy"),i.disabled=!1,!s){i.dataset.error="1",vn(i,lb),window.setTimeout(()=>{i.isConnected&&(delete i.dataset.error,vn(i,t))},ab);return}i.dataset.copied="1",vn(i,ob),window.setTimeout(()=>{i.isConnected&&(delete i.dataset.copied,vn(i,t))},sb)}}}
    >
      <span class="chat-copy-btn__icon" aria-hidden="true">
        <span class="chat-copy-btn__icon-copy">${J.copy}</span>
        <span class="chat-copy-btn__icon-check">${J.check}</span>
      </span>
    </button>
  `}function db(e){return cb({text:()=>e,label:_r})}function Cr(e){const t=e;let n=typeof t.role=="string"?t.role:"unknown";const i=typeof t.toolCallId=="string"||typeof t.tool_call_id=="string",s=t.content,a=Array.isArray(s)?s:null,o=Array.isArray(a)&&a.some(u=>{const y=u,v=(typeof y.type=="string"?y.type:"").toLowerCase();return v==="toolresult"||v==="tool_result"}),l=typeof t.toolName=="string"||typeof t.tool_name=="string";(i||o||l)&&(n="toolResult");let d=[];typeof t.content=="string"?d=[{type:"text",text:t.content}]:Array.isArray(t.content)?d=t.content.map(u=>({type:u.type||"text",text:u.text,name:u.name,args:u.args||u.arguments})):typeof t.text=="string"&&(d=[{type:"text",text:t.text}]);const h=typeof t.timestamp=="number"?t.timestamp:Date.now(),p=typeof t.id=="string"?t.id:void 0;return{role:n,content:d,timestamp:h,id:p}}function Gs(e){const t=e.toLowerCase();return e==="user"||e==="User"?e:e==="assistant"?"assistant":e==="system"?"system":t==="toolresult"||t==="tool_result"||t==="tool"||t==="function"?"tool":e}function Er(e){const t=e,n=typeof t.role=="string"?t.role.toLowerCase():"";return n==="toolresult"||n==="tool_result"}const ub={icon:"puzzle",detailKeys:["command","path","url","targetUrl","targetId","ref","element","node","nodeId","id","requestId","to","channelId","guildId","userId","name","query","pattern","messageId"]},fb={bash:{icon:"wrench",title:"Bash",detailKeys:["command"]},process:{icon:"wrench",title:"Process",detailKeys:["sessionId"]},read:{icon:"fileText",title:"Read",detailKeys:["path"]},write:{icon:"edit",title:"Write",detailKeys:["path"]},edit:{icon:"penLine",title:"Edit",detailKeys:["path"]},attach:{icon:"paperclip",title:"Attach",detailKeys:["path","url","fileName"]},browser:{icon:"globe",title:"Browser",actions:{status:{label:"status"},start:{label:"start"},stop:{label:"stop"},tabs:{label:"tabs"},open:{label:"open",detailKeys:["targetUrl"]},focus:{label:"focus",detailKeys:["targetId"]},close:{label:"close",detailKeys:["targetId"]},snapshot:{label:"snapshot",detailKeys:["targetUrl","targetId","ref","element","format"]},screenshot:{label:"screenshot",detailKeys:["targetUrl","targetId","ref","element"]},navigate:{label:"navigate",detailKeys:["targetUrl","targetId"]},console:{label:"console",detailKeys:["level","targetId"]},pdf:{label:"pdf",detailKeys:["targetId"]},upload:{label:"upload",detailKeys:["paths","ref","inputRef","element","targetId"]},dialog:{label:"dialog",detailKeys:["accept","promptText","targetId"]},act:{label:"act",detailKeys:["request.kind","request.ref","request.selector","request.text","request.value"]}}},canvas:{icon:"image",title:"Canvas",actions:{present:{label:"present",detailKeys:["target","node","nodeId"]},hide:{label:"hide",detailKeys:["node","nodeId"]},navigate:{label:"navigate",detailKeys:["url","node","nodeId"]},eval:{label:"eval",detailKeys:["javaScript","node","nodeId"]},snapshot:{label:"snapshot",detailKeys:["format","node","nodeId"]},a2ui_push:{label:"A2UI push",detailKeys:["jsonlPath","node","nodeId"]},a2ui_reset:{label:"A2UI reset",detailKeys:["node","nodeId"]}}},nodes:{icon:"smartphone",title:"Nodes",actions:{status:{label:"status"},describe:{label:"describe",detailKeys:["node","nodeId"]},pending:{label:"pending"},approve:{label:"approve",detailKeys:["requestId"]},reject:{label:"reject",detailKeys:["requestId"]},notify:{label:"notify",detailKeys:["node","nodeId","title","body"]},camera_snap:{label:"camera snap",detailKeys:["node","nodeId","facing","deviceId"]},camera_list:{label:"camera list",detailKeys:["node","nodeId"]},camera_clip:{label:"camera clip",detailKeys:["node","nodeId","facing","duration","durationMs"]},screen_record:{label:"screen record",detailKeys:["node","nodeId","duration","durationMs","fps","screenIndex"]}}},cron:{icon:"loader",title:"Cron",actions:{status:{label:"status"},list:{label:"list"},add:{label:"add",detailKeys:["job.name","job.id","job.schedule","job.cron"]},update:{label:"update",detailKeys:["id"]},remove:{label:"remove",detailKeys:["id"]},run:{label:"run",detailKeys:["id"]},runs:{label:"runs",detailKeys:["id"]},wake:{label:"wake",detailKeys:["text","mode"]}}},gateway:{icon:"plug",title:"Gateway",actions:{restart:{label:"restart",detailKeys:["reason","delayMs"]},"config.get":{label:"config get"},"config.schema":{label:"config schema"},"config.apply":{label:"config apply",detailKeys:["restartDelayMs"]},"update.run":{label:"update run",detailKeys:["restartDelayMs"]}}},whatsapp_login:{icon:"circle",title:"WhatsApp Login",actions:{start:{label:"start"},wait:{label:"wait"}}},discord:{icon:"messageSquare",title:"Discord",actions:{react:{label:"react",detailKeys:["channelId","messageId","emoji"]},reactions:{label:"reactions",detailKeys:["channelId","messageId"]},sticker:{label:"sticker",detailKeys:["to","stickerIds"]},poll:{label:"poll",detailKeys:["question","to"]},permissions:{label:"permissions",detailKeys:["channelId"]},readMessages:{label:"read messages",detailKeys:["channelId","limit"]},sendMessage:{label:"send",detailKeys:["to","content"]},editMessage:{label:"edit",detailKeys:["channelId","messageId"]},deleteMessage:{label:"delete",detailKeys:["channelId","messageId"]},threadCreate:{label:"thread create",detailKeys:["channelId","name"]},threadList:{label:"thread list",detailKeys:["guildId","channelId"]},threadReply:{label:"thread reply",detailKeys:["channelId","content"]},pinMessage:{label:"pin",detailKeys:["channelId","messageId"]},unpinMessage:{label:"unpin",detailKeys:["channelId","messageId"]},listPins:{label:"list pins",detailKeys:["channelId"]},searchMessages:{label:"search",detailKeys:["guildId","content"]},memberInfo:{label:"member",detailKeys:["guildId","userId"]},roleInfo:{label:"roles",detailKeys:["guildId"]},emojiList:{label:"emoji list",detailKeys:["guildId"]},roleAdd:{label:"role add",detailKeys:["guildId","userId","roleId"]},roleRemove:{label:"role remove",detailKeys:["guildId","userId","roleId"]},channelInfo:{label:"channel",detailKeys:["channelId"]},channelList:{label:"channels",detailKeys:["guildId"]},voiceStatus:{label:"voice",detailKeys:["guildId","userId"]},eventList:{label:"events",detailKeys:["guildId"]},eventCreate:{label:"event create",detailKeys:["guildId","name"]},timeout:{label:"timeout",detailKeys:["guildId","userId"]},kick:{label:"kick",detailKeys:["guildId","userId"]},ban:{label:"ban",detailKeys:["guildId","userId"]}}},slack:{icon:"messageSquare",title:"Slack",actions:{react:{label:"react",detailKeys:["channelId","messageId","emoji"]},reactions:{label:"reactions",detailKeys:["channelId","messageId"]},sendMessage:{label:"send",detailKeys:["to","content"]},editMessage:{label:"edit",detailKeys:["channelId","messageId"]},deleteMessage:{label:"delete",detailKeys:["channelId","messageId"]},readMessages:{label:"read messages",detailKeys:["channelId","limit"]},pinMessage:{label:"pin",detailKeys:["channelId","messageId"]},unpinMessage:{label:"unpin",detailKeys:["channelId","messageId"]},listPins:{label:"list pins",detailKeys:["channelId"]},memberInfo:{label:"member",detailKeys:["userId"]},emojiList:{label:"emoji list"}}}},gb={fallback:ub,tools:fb},Tr=gb,To=Tr.fallback??{icon:"puzzle"},hb=Tr.tools??{};function pb(e){return(e??"tool").trim()}function vb(e){const t=e.replace(/_/g," ").trim();return t?t.split(/\s+/).map(n=>n.length<=2&&n.toUpperCase()===n?n:`${n.at(0)?.toUpperCase()??""}${n.slice(1)}`).join(" "):"Tool"}function mb(e){const t=e?.trim();if(t)return t.replace(/_/g," ")}function Lr(e){if(e!=null){if(typeof e=="string"){const t=e.trim();if(!t)return;const n=t.split(/\r?\n/)[0]?.trim()??"";return n?n.length>160?`${n.slice(0,157)}…`:n:void 0}if(typeof e=="number"||typeof e=="boolean")return String(e);if(Array.isArray(e)){const t=e.map(i=>Lr(i)).filter(i=>!!i);if(t.length===0)return;const n=t.slice(0,3).join(", ");return t.length>3?`${n}…`:n}}}function bb(e,t){if(!e||typeof e!="object")return;let n=e;for(const i of t.split(".")){if(!i||!n||typeof n!="object")return;n=n[i]}return n}function yb(e,t){for(const n of t){const i=bb(e,n),s=Lr(i);if(s)return s}}function wb(e){if(!e||typeof e!="object")return;const t=e,n=typeof t.path=="string"?t.path:void 0;if(!n)return;const i=typeof t.offset=="number"?t.offset:void 0,s=typeof t.limit=="number"?t.limit:void 0;return i!==void 0&&s!==void 0?`${n}:${i}-${i+s}`:n}function $b(e){if(!e||typeof e!="object")return;const t=e;return typeof t.path=="string"?t.path:void 0}function kb(e,t){if(!(!e||!t))return e.actions?.[t]??void 0}function Ab(e){const t=pb(e.name),n=t.toLowerCase(),i=hb[n],s=i?.icon??To.icon??"puzzle",a=i?.title??vb(t),o=i?.label??t,l=e.args&&typeof e.args=="object"?e.args.action:void 0,d=typeof l=="string"?l.trim():void 0,h=kb(i,d),p=mb(h?.label??d);let u;n==="read"&&(u=wb(e.args)),!u&&(n==="write"||n==="edit"||n==="attach")&&(u=$b(e.args));const y=h?.detailKeys??i?.detailKeys??To.detailKeys??[];return!u&&y.length>0&&(u=yb(e.args,y)),!u&&e.meta&&(u=e.meta),u&&(u=xb(u)),{name:t,icon:s,title:a,label:o,verb:p,detail:u}}function Sb(e){const t=[];if(e.verb&&t.push(e.verb),e.detail&&t.push(e.detail),t.length!==0)return t.join(" · ")}function xb(e){return e&&e.replace(/\/Users\/[^/]+/g,"~").replace(/\/home\/[^/]+/g,"~")}const _b=80,Cb=2,Lo=100;function Eb(e){const t=e.trim();if(t.startsWith("{")||t.startsWith("["))try{const n=JSON.parse(t);return"```json\n"+JSON.stringify(n,null,2)+"\n```"}catch{}return e}function Tb(e){const t=e.split(`
`),n=t.slice(0,Cb),i=n.join(`
`);return i.length>Lo?i.slice(0,Lo)+"…":n.length<t.length?i+"…":i}function Lb(e){const t=e,n=Ib(t.content),i=[];for(const s of n){const a=(typeof s.type=="string"?s.type:"").toLowerCase();(["toolcall","tool_call","tooluse","tool_use"].includes(a)||typeof s.name=="string"&&s.arguments!=null)&&i.push({kind:"call",name:s.name??"tool",args:Rb(s.arguments??s.args)})}for(const s of n){const a=(typeof s.type=="string"?s.type:"").toLowerCase();if(a!=="toolresult"&&a!=="tool_result")continue;const o=Mb(s),l=typeof s.name=="string"?s.name:"tool";i.push({kind:"result",name:l,text:o})}if(Er(e)&&!i.some(s=>s.kind==="result")){const s=typeof t.toolName=="string"&&t.toolName||typeof t.tool_name=="string"&&t.tool_name||"tool",a=Ul(e)??void 0;i.push({kind:"result",name:s,text:a})}return i}function Io(e,t){const n=Ab({name:e.name,args:e.args}),i=Sb(n),s=!!e.text?.trim(),a=!!t,o=a?()=>{if(s){t(Eb(e.text));return}const u=`## ${n.label}

${i?`**Command:** \`${i}\`

`:""}*No output — tool completed successfully.*`;t(u)}:void 0,l=s&&(e.text?.length??0)<=_b,d=s&&!l,h=s&&l,p=!s;return r`
    <div
      class="chat-tool-card ${a?"chat-tool-card--clickable":""}"
      @click=${o}
      role=${a?"button":m}
      tabindex=${a?"0":m}
      @keydown=${a?u=>{u.key!=="Enter"&&u.key!==" "||(u.preventDefault(),o?.())}:m}
    >
      <div class="chat-tool-card__header">
        <div class="chat-tool-card__title">
          <span class="chat-tool-card__icon">${J[n.icon]}</span>
          <span>${n.label}</span>
        </div>
        ${a?r`<span class="chat-tool-card__action">${s?"View":""} ${J.check}</span>`:m}
        ${p&&!a?r`<span class="chat-tool-card__status">${J.check}</span>`:m}
      </div>
      ${i?r`<div class="chat-tool-card__detail">${i}</div>`:m}
      ${p?r`
              <div class="chat-tool-card__status-text muted">Completed</div>
            `:m}
      ${d?r`<div class="chat-tool-card__preview mono">${Tb(e.text)}</div>`:m}
      ${h?r`<div class="chat-tool-card__inline mono">${e.text}</div>`:m}
    </div>
  `}function Ib(e){return Array.isArray(e)?e.filter(Boolean):[]}function Rb(e){if(typeof e!="string")return e;const t=e.trim();if(!t||!t.startsWith("{")&&!t.startsWith("["))return e;try{return JSON.parse(t)}catch{return e}}function Mb(e){if(typeof e.text=="string")return e.text;if(typeof e.content=="string")return e.content}function Pb(e){const n=e.content,i=[];if(Array.isArray(n))for(const s of n){if(typeof s!="object"||s===null)continue;const a=s;if(a.type==="image"){const o=a.source;if(o?.type==="base64"&&typeof o.data=="string"){const l=o.data,d=o.media_type||"image/png",h=l.startsWith("data:")?l:`data:${d};base64,${l}`;i.push({url:h})}else typeof a.url=="string"&&i.push({url:a.url})}else if(a.type==="image_url"){const o=a.image_url;typeof o?.url=="string"&&i.push({url:o.url})}}return i}function Fb(e){return r`
    <div class="chat-group assistant">
      ${Ws("assistant",e)}
      <div class="chat-group-messages">
        <div class="chat-bubble chat-reading-indicator" aria-hidden="true">
          <span class="chat-reading-indicator__dots">
            <span></span><span></span><span></span>
          </span>
        </div>
      </div>
    </div>
  `}function Nb(e,t,n,i){const s=new Date(t).toLocaleTimeString([],{hour:"numeric",minute:"2-digit"}),a=i?.name??"Assistant";return r`
    <div class="chat-group assistant">
      ${Ws("assistant",i)}
      <div class="chat-group-messages">
        ${Ir({role:"assistant",content:[{type:"text",text:e}],timestamp:t},{isStreaming:!0,showReasoning:!1},n)}
        <div class="chat-group-footer">
          <span class="chat-sender-name">${a}</span>
          <span class="chat-group-timestamp">${s}</span>
        </div>
      </div>
    </div>
  `}function Ob(e,t){const n=Gs(e.role),i=t.assistantName??"Assistant",s=n==="user"?"You":n==="assistant"?i:n,a=n==="user"?"user":n==="assistant"?"assistant":"other",o=new Date(e.timestamp).toLocaleTimeString([],{hour:"numeric",minute:"2-digit"});return r`
    <div class="chat-group ${a}">
      ${Ws(e.role,{name:i,avatar:t.assistantAvatar??null})}
      <div class="chat-group-messages">
        ${e.messages.map((l,d)=>Ir(l.message,{isStreaming:e.isStreaming&&d===e.messages.length-1,showReasoning:t.showReasoning},t.onOpenSidebar))}
        <div class="chat-group-footer">
          <span class="chat-sender-name">${s}</span>
          <span class="chat-group-timestamp">${o}</span>
        </div>
      </div>
    </div>
  `}function Ws(e,t){const n=Gs(e),i=t?.name?.trim()||"Assistant",s=t?.avatar?.trim()||"",a=n==="user"?"U":n==="assistant"?i.charAt(0).toUpperCase()||"A":n==="tool"?"⚙":"?",o=n==="user"?"user":n==="assistant"?"assistant":n==="tool"?"tool":"other";return s&&n==="assistant"?Db(s)?r`<img
        class="chat-avatar ${o}"
        src="${s}"
        alt="${i}"
      />`:r`<div class="chat-avatar ${o}">${s}</div>`:r`<div class="chat-avatar ${o}">${a}</div>`}function Db(e){return/^https?:\/\//i.test(e)||/^data:image\//i.test(e)||e.startsWith("/")}function Bb(e){return e.length===0?m:r`
    <div class="chat-message-images">
      ${e.map(t=>r`
          <img
            src=${t.url}
            alt=${t.alt??"Attached image"}
            class="chat-message-image"
            @click=${()=>window.open(t.url,"_blank")}
          />
        `)}
    </div>
  `}function Ir(e,t,n){const i=e,s=typeof i.role=="string"?i.role:"unknown",a=Er(e)||s.toLowerCase()==="toolresult"||s.toLowerCase()==="tool_result"||typeof i.toolCallId=="string"||typeof i.tool_call_id=="string",o=Lb(e),l=o.length>0,d=Pb(e),h=d.length>0,p=Ul(e),u=t.showReasoning&&s==="assistant"?kh(e):null,y=p?.trim()?p:null,v=u?Sh(u):null,$=y,g=s==="assistant"&&!!$?.trim(),w=["chat-bubble",g?"has-copy":"",t.isStreaming?"streaming":"","fade-in"].filter(Boolean).join(" ");return!$&&l&&a?r`${o.map(_=>Io(_,n))}`:!$&&!l&&!h?m:r`
    <div class="${w}">
      ${g?db($):m}
      ${Bb(d)}
      ${v?r`<div class="chat-thinking">${Yi(is(v))}</div>`:m}
      ${$?r`<div class="chat-text">${Yi(is($))}</div>`:m}
      ${o.map(_=>Io(_,n))}
    </div>
  `}function Ub(e){return r`
    <div class="sidebar-panel">
      <div class="sidebar-header">
        <div class="sidebar-title">Tool Output</div>
        <button @click=${e.onClose} class="btn" title="Close sidebar">
          ${J.x}
        </button>
      </div>
      <div class="sidebar-content">
        ${e.error?r`
              <div class="callout danger">${e.error}</div>
              <button @click=${e.onViewRawText} class="btn" style="margin-top: 12px;">
                View Raw Text
              </button>
            `:e.content?r`<div class="sidebar-markdown">${Yi(is(e.content))}</div>`:r`
                  <div class="muted">No content available</div>
                `}
      </div>
    </div>
  `}var Kb=Object.create,qs=Object.defineProperty,zb=Object.getOwnPropertyDescriptor,Rr=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),Jt=e=>{throw TypeError(e)},Hb=(e,t,n)=>t in e?qs(e,t,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[t]=n,Ro=(e,t)=>qs(e,"name",{value:t,configurable:!0}),jb=e=>[,,,Kb(e?.[Rr("metadata")]??null)],Mr=["class","method","getter","setter","accessor","field","value","get","set"],It=e=>e!==void 0&&typeof e!="function"?Jt("Function expected"):e,Gb=(e,t,n,i,s)=>({kind:Mr[e],name:t,metadata:i,addInitializer:a=>n._?Jt("Already initialized"):s.push(It(a||null))}),Wb=(e,t)=>Hb(t,Rr("metadata"),e[3]),qe=(e,t,n,i)=>{for(var s=0,a=e[t>>1],o=a&&a.length;s<o;s++)t&1?a[s].call(n):i=a[s].call(n,i);return i},Yn=(e,t,n,i,s,a)=>{var o,l,d,h,p,u=t&7,y=!!(t&8),v=!!(t&16),$=u>3?e.length+1:u?y?1:2:0,g=Mr[u+5],w=u>3&&(e[$-1]=[]),_=e[$]||(e[$]=[]),C=u&&(!v&&!y&&(s=s.prototype),u<5&&(u>3||!v)&&zb(u<4?s:{get[n](){return Mo(this,a)},set[n](x){return Po(this,a,x)}},n));u?v&&u<4&&Ro(a,(u>2?"set ":u>1?"get ":"")+n):Ro(s,n);for(var L=i.length-1;L>=0;L--)h=Gb(u,n,d={},e[3],_),u&&(h.static=y,h.private=v,p=h.access={has:v?x=>qb(s,x):x=>n in x},u^3&&(p.get=v?x=>(u^1?Mo:Vb)(x,s,u^4?a:C.get):x=>x[n]),u>2&&(p.set=v?(x,T)=>Po(x,s,T,u^4?a:C.set):(x,T)=>x[n]=T)),l=(0,i[L])(u?u<4?v?a:C[g]:u>4?void 0:{get:C.get,set:C.set}:s,h),d._=1,u^4||l===void 0?It(l)&&(u>4?w.unshift(l):u?v?a=l:C[g]=l:s=l):typeof l!="object"||l===null?Jt("Object expected"):(It(o=l.get)&&(C.get=o),It(o=l.set)&&(C.set=o),It(o=l.init)&&w.unshift(o));return u||Wb(e,s),C&&qs(s,n,C),v?u^4?a:C:s},Vs=(e,t,n)=>t.has(e)||Jt("Cannot "+n),qb=(e,t)=>Object(t)!==t?Jt('Cannot use the "in" operator on this value'):e.has(t),Mo=(e,t,n)=>(Vs(e,t,"read from private field"),n?n.call(e):t.get(e)),Po=(e,t,n,i)=>(Vs(e,t,"write to private field"),i?i.call(e,n):t.set(e,n),n),Vb=(e,t,n)=>(Vs(e,t,"access private method"),n),Pr,Fr,Nr,ss,Or,ce;Or=[tl("resizable-divider")];class tt extends(ss=gt,Nr=[yn({type:Number})],Fr=[yn({type:Number})],Pr=[yn({type:Number})],ss){constructor(){super(...arguments),this.splitRatio=qe(ce,8,this,.6),qe(ce,11,this),this.minRatio=qe(ce,12,this,.4),qe(ce,15,this),this.maxRatio=qe(ce,16,this,.7),qe(ce,19,this),this.isDragging=!1,this.startX=0,this.startRatio=0,this.handleMouseDown=t=>{this.isDragging=!0,this.startX=t.clientX,this.startRatio=this.splitRatio,this.classList.add("dragging"),document.addEventListener("mousemove",this.handleMouseMove),document.addEventListener("mouseup",this.handleMouseUp),t.preventDefault()},this.handleMouseMove=t=>{if(!this.isDragging)return;const n=this.parentElement;if(!n)return;const i=n.getBoundingClientRect().width,a=(t.clientX-this.startX)/i;let o=this.startRatio+a;o=Math.max(this.minRatio,Math.min(this.maxRatio,o)),this.dispatchEvent(new CustomEvent("resize",{detail:{splitRatio:o},bubbles:!0,composed:!0}))},this.handleMouseUp=()=>{this.isDragging=!1,this.classList.remove("dragging"),document.removeEventListener("mousemove",this.handleMouseMove),document.removeEventListener("mouseup",this.handleMouseUp)}}render(){return m}connectedCallback(){super.connectedCallback(),this.addEventListener("mousedown",this.handleMouseDown)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("mousedown",this.handleMouseDown),document.removeEventListener("mousemove",this.handleMouseMove),document.removeEventListener("mouseup",this.handleMouseUp)}}ce=jb(ss);Yn(ce,5,"splitRatio",Nr,tt);Yn(ce,5,"minRatio",Fr,tt);Yn(ce,5,"maxRatio",Pr,tt);tt=Yn(ce,0,"ResizableDivider",Or,tt);tt.styles=Ou`
    :host {
      width: 4px;
      cursor: col-resize;
      background: var(--border, #333);
      transition: background 150ms ease-out;
      flex-shrink: 0;
      position: relative;
    }
    :host::before {
      content: "";
      position: absolute;
      top: 0;
      left: -4px;
      right: -4px;
      bottom: 0;
    }
    :host(:hover) {
      background: var(--accent, #007bff);
    }
    :host(.dragging) {
      background: var(--accent, #007bff);
    }
  `;qe(ce,1,tt);const Yb=5e3;function Fo(e){e.style.height="auto",e.style.height=`${e.scrollHeight}px`}function Qb(e){return e?e.active?r`
      <div class="callout info compaction-indicator compaction-indicator--active">
        ${J.loader} Compacting context...
      </div>
    `:e.completedAt&&Date.now()-e.completedAt<Yb?r`
        <div class="callout success compaction-indicator compaction-indicator--complete">
          ${J.check} Context compacted
        </div>
      `:m:m}function Jb(){return`att-${Date.now()}-${Math.random().toString(36).slice(2,9)}`}function Zb(e,t){const n=e.clipboardData?.items;if(!n||!t.onAttachmentsChange)return;const i=[];for(let s=0;s<n.length;s++){const a=n[s];a.type.startsWith("image/")&&i.push(a)}if(i.length!==0){e.preventDefault();for(const s of i){const a=s.getAsFile();if(!a)continue;const o=new FileReader;o.addEventListener("load",()=>{const l=o.result,d={id:Jb(),dataUrl:l,mimeType:a.type},h=t.attachments??[];t.onAttachmentsChange?.([...h,d])}),o.readAsDataURL(a)}}}function Xb(e){const t=e.attachments??[];return t.length===0?m:r`
    <div class="chat-attachments">
      ${t.map(n=>r`
          <div class="chat-attachment">
            <img
              src=${n.dataUrl}
              alt="Attachment preview"
              class="chat-attachment__img"
            />
            <button
              class="chat-attachment__remove"
              type="button"
              aria-label="Remove attachment"
              @click=${()=>{const i=(e.attachments??[]).filter(s=>s.id!==n.id);e.onAttachmentsChange?.(i)}}
            >
              ${J.x}
            </button>
          </div>
        `)}
    </div>
  `}function ey(e){const t=e.connected,n=e.sending||e.stream!==null,i=!!(e.canAbort&&e.onAbort),a=e.sessions?.sessions?.find(v=>v.key===e.sessionKey)?.reasoningLevel??"off",o=e.showThinking&&a!=="off",l={name:e.assistantName,avatar:e.assistantAvatar??e.assistantAvatarUrl??null},d=(e.attachments?.length??0)>0,h=e.connected?d?"Add a message or paste more images...":"Message (↩ to send, Shift+↩ for line breaks, paste images)":"Connect to the gateway to start chatting…",p=e.splitRatio??.6,u=!!(e.sidebarOpen&&e.onCloseSidebar),y=r`
    <div
      class="chat-thread"
      role="log"
      aria-live="polite"
      @scroll=${e.onChatScroll}
    >
      ${e.loading?r`
              <div class="muted">Loading chat…</div>
            `:m}
      ${Jl(ny(e),v=>v.key,v=>v.kind==="reading-indicator"?Fb(l):v.kind==="stream"?Nb(v.text,v.startedAt,e.onOpenSidebar,l):v.kind==="group"?Ob(v,{onOpenSidebar:e.onOpenSidebar,showReasoning:o,assistantName:e.assistantName,assistantAvatar:l.avatar}):m)}
    </div>
  `;return r`
    <section class="card chat">
      ${e.disabledReason?r`<div class="callout">${e.disabledReason}</div>`:m}

      ${e.error?r`<div class="callout danger">${e.error}</div>`:m}

      ${Qb(e.compactionStatus)}

      ${e.focusMode?r`
            <button
              class="chat-focus-exit"
              type="button"
              @click=${e.onToggleFocusMode}
              aria-label="Exit focus mode"
              title="Exit focus mode"
            >
              ${J.x}
            </button>
          `:m}

      <div
        class="chat-split-container ${u?"chat-split-container--open":""}"
      >
        <div
          class="chat-main"
          style="flex: ${u?`0 0 ${p*100}%`:"1 1 100%"}"
        >
          ${y}
        </div>

        ${u?r`
              <resizable-divider
                .splitRatio=${p}
                @resize=${v=>e.onSplitRatioChange?.(v.detail.splitRatio)}
              ></resizable-divider>
              <div class="chat-sidebar">
                ${Ub({content:e.sidebarContent??null,error:e.sidebarError??null,onClose:e.onCloseSidebar,onViewRawText:()=>{!e.sidebarContent||!e.onOpenSidebar||e.onOpenSidebar(`\`\`\`
${e.sidebarContent}
\`\`\``)}})}
              </div>
            `:m}
      </div>

      ${e.queue.length?r`
            <div class="chat-queue" role="status" aria-live="polite">
              <div class="chat-queue__title">Queued (${e.queue.length})</div>
              <div class="chat-queue__list">
                ${e.queue.map(v=>r`
                    <div class="chat-queue__item">
                      <div class="chat-queue__text">
                        ${v.text||(v.attachments?.length?`Image (${v.attachments.length})`:"")}
                      </div>
                      <button
                        class="btn chat-queue__remove"
                        type="button"
                        aria-label="Remove queued message"
                        @click=${()=>e.onQueueRemove(v.id)}
                      >
                        ${J.x}
                      </button>
                    </div>
                  `)}
              </div>
            </div>
          `:m}

      ${e.showNewMessages?r`
            <button
              class="btn chat-new-messages"
              type="button"
              @click=${e.onScrollToBottom}
            >
              New messages ${J.arrowDown}
            </button>
          `:m}

      <div class="chat-compose">
        ${Xb(e)}
        <div class="chat-compose__row">
          <label class="field chat-compose__field">
            <span>Message</span>
            <textarea
              ${qv(v=>v&&Fo(v))}
              .value=${e.draft}
              ?disabled=${!e.connected}
              @keydown=${v=>{v.key==="Enter"&&(v.isComposing||v.keyCode===229||v.shiftKey||e.connected&&(v.preventDefault(),t&&e.onSend()))}}
              @input=${v=>{const $=v.target;Fo($),e.onDraftChange($.value)}}
              @paste=${v=>Zb(v,e)}
              placeholder=${h}
            ></textarea>
          </label>
          <div class="chat-compose__actions">
            <button
              class="btn"
              ?disabled=${!e.connected||!i&&e.sending}
              @click=${i?e.onAbort:e.onNewSession}
            >
              ${i?"Stop":"New session"}
            </button>
            <button
              class="btn primary"
              ?disabled=${!e.connected}
              @click=${e.onSend}
            >
              ${n?"Queue":"Send"}<kbd class="btn-kbd">↵</kbd>
            </button>
          </div>
        </div>
      </div>
    </section>
  `}const No=200;function ty(e){const t=[];let n=null;for(const i of e){if(i.kind!=="message"){n&&(t.push(n),n=null),t.push(i);continue}const s=Cr(i.message),a=Gs(s.role),o=s.timestamp||Date.now();!n||n.role!==a?(n&&t.push(n),n={kind:"group",key:`group:${a}:${i.key}`,role:a,messages:[{message:i.message,key:i.key}],timestamp:o,isStreaming:!1}):n.messages.push({message:i.message,key:i.key})}return n&&t.push(n),t}function ny(e){const t=[],n=Array.isArray(e.messages)?e.messages:[],i=Array.isArray(e.toolMessages)?e.toolMessages:[],s=Math.max(0,n.length-No);s>0&&t.push({kind:"message",key:"chat:history:notice",message:{role:"system",content:`Showing last ${No} messages (${s} hidden).`,timestamp:Date.now()}});for(let a=s;a<n.length;a++){const o=n[a],l=Cr(o);!e.showThinking&&l.role.toLowerCase()==="toolresult"||t.push({kind:"message",key:Oo(o,a),message:o})}if(e.showThinking)for(let a=0;a<i.length;a++)t.push({kind:"message",key:Oo(i[a],a+n.length),message:i[a]});if(e.stream!==null){const a=`stream:${e.sessionKey}:${e.streamStartedAt??"live"}`;e.stream.trim().length>0?t.push({kind:"stream",key:a,text:e.stream,startedAt:e.streamStartedAt??Date.now()}):t.push({kind:"reading-indicator",key:a})}return ty(t)}function Oo(e,t){const n=e,i=typeof n.toolCallId=="string"?n.toolCallId:"";if(i)return`tool:${i}`;const s=typeof n.id=="string"?n.id:"";if(s)return`msg:${s}`;const a=typeof n.messageId=="string"?n.messageId:"";if(a)return`msg:${a}`;const o=typeof n.timestamp=="number"?n.timestamp:null,l=typeof n.role=="string"?n.role:"unknown";return o!=null?`msg:${l}:${o}:${t}`:`msg:${l}:${t}`}const as={all:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="3" width="7" height="7"></rect>
      <rect x="14" y="3" width="7" height="7"></rect>
      <rect x="14" y="14" width="7" height="7"></rect>
      <rect x="3" y="14" width="7" height="7"></rect>
    </svg>
  `,env:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="3"></circle>
      <path
        d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
      ></path>
    </svg>
  `,update:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
      <polyline points="7 10 12 15 17 10"></polyline>
      <line x1="12" y1="15" x2="12" y2="3"></line>
    </svg>
  `,agents:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path
        d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z"
      ></path>
      <circle cx="8" cy="14" r="1"></circle>
      <circle cx="16" cy="14" r="1"></circle>
    </svg>
  `,auth:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
    </svg>
  `,channels:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
    </svg>
  `,messages:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
      <polyline points="22,6 12,13 2,6"></polyline>
    </svg>
  `,commands:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polyline points="4 17 10 11 4 5"></polyline>
      <line x1="12" y1="19" x2="20" y2="19"></line>
    </svg>
  `,hooks:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
    </svg>
  `,skills:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <polygon
        points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
      ></polygon>
    </svg>
  `,tools:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path
        d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
      ></path>
    </svg>
  `,gateway:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path
        d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
      ></path>
    </svg>
  `,wizard:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M15 4V2"></path>
      <path d="M15 16v-2"></path>
      <path d="M8 9h2"></path>
      <path d="M20 9h2"></path>
      <path d="M17.8 11.8 19 13"></path>
      <path d="M15 9h0"></path>
      <path d="M17.8 6.2 19 5"></path>
      <path d="m3 21 9-9"></path>
      <path d="M12.2 6.2 11 5"></path>
    </svg>
  `,meta:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 20h9"></path>
      <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"></path>
    </svg>
  `,logging:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
      <line x1="16" y1="13" x2="8" y2="13"></line>
      <line x1="16" y1="17" x2="8" y2="17"></line>
      <polyline points="10 9 9 9 8 9"></polyline>
    </svg>
  `,browser:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <circle cx="12" cy="12" r="4"></circle>
      <line x1="21.17" y1="8" x2="12" y2="8"></line>
      <line x1="3.95" y1="6.06" x2="8.54" y2="14"></line>
      <line x1="10.88" y1="21.94" x2="15.46" y2="14"></line>
    </svg>
  `,ui:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
      <line x1="3" y1="9" x2="21" y2="9"></line>
      <line x1="9" y1="21" x2="9" y2="9"></line>
    </svg>
  `,models:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path
        d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"
      ></path>
      <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
      <line x1="12" y1="22.08" x2="12" y2="12"></line>
    </svg>
  `,bindings:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
      <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
      <line x1="6" y1="6" x2="6.01" y2="6"></line>
      <line x1="6" y1="18" x2="6.01" y2="18"></line>
    </svg>
  `,broadcast:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"></path>
      <path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"></path>
      <circle cx="12" cy="12" r="2"></circle>
      <path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"></path>
      <path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"></path>
    </svg>
  `,audio:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M9 18V5l12-2v13"></path>
      <circle cx="6" cy="18" r="3"></circle>
      <circle cx="18" cy="16" r="3"></circle>
    </svg>
  `,session:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
      <circle cx="9" cy="7" r="4"></circle>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
    </svg>
  `,cron:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <polyline points="12 6 12 12 16 14"></polyline>
    </svg>
  `,web:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="2" y1="12" x2="22" y2="12"></line>
      <path
        d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"
      ></path>
    </svg>
  `,discovery:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
  `,canvasHost:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
      <circle cx="8.5" cy="8.5" r="1.5"></circle>
      <polyline points="21 15 16 10 5 21"></polyline>
    </svg>
  `,talk:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
      <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
      <line x1="12" y1="19" x2="12" y2="23"></line>
      <line x1="8" y1="23" x2="16" y2="23"></line>
    </svg>
  `,plugins:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M12 2v6"></path>
      <path d="m4.93 10.93 4.24 4.24"></path>
      <path d="M2 12h6"></path>
      <path d="m4.93 13.07 4.24-4.24"></path>
      <path d="M12 22v-6"></path>
      <path d="m19.07 13.07-4.24-4.24"></path>
      <path d="M22 12h-6"></path>
      <path d="m19.07 10.93-4.24 4.24"></path>
    </svg>
  `,default:r`
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
      <polyline points="14 2 14 8 20 8"></polyline>
    </svg>
  `},Do=[{key:"env",label:"Environment"},{key:"update",label:"Updates"},{key:"agents",label:"Agents"},{key:"auth",label:"Authentication"},{key:"channels",label:"Channels"},{key:"messages",label:"Messages"},{key:"commands",label:"Commands"},{key:"hooks",label:"Hooks"},{key:"skills",label:"Skills"},{key:"tools",label:"Tools"},{key:"gateway",label:"Gateway"},{key:"wizard",label:"Setup Wizard"}],Bo="__all__";function Uo(e){return as[e]??as.default}function iy(e,t){const n=Fs[e];return n||{label:t?.title??Ie(e),description:t?.description??""}}function sy(e){const{key:t,schema:n,uiHints:i}=e;if(!n||Se(n)!=="object"||!n.properties)return[];const s=Object.entries(n.properties).map(([a,o])=>{const l=de([t,a],i),d=l?.label??o.title??Ie(a),h=l?.help??o.description??"",p=l?.order??50;return{key:a,label:d,description:h,order:p}});return s.sort((a,o)=>a.order!==o.order?a.order-o.order:a.key.localeCompare(o.key)),s}function ay(e,t){if(!e||!t)return[];const n=[];function i(s,a,o){if(s===a)return;if(typeof s!=typeof a){n.push({path:o,from:s,to:a});return}if(typeof s!="object"||s===null||a===null){s!==a&&n.push({path:o,from:s,to:a});return}if(Array.isArray(s)&&Array.isArray(a)){JSON.stringify(s)!==JSON.stringify(a)&&n.push({path:o,from:s,to:a});return}const l=s,d=a,h=new Set([...Object.keys(l),...Object.keys(d)]);for(const p of h)i(l[p],d[p],o?`${o}.${p}`:p)}return i(e,t,""),n}function Ko(e,t=40){let n;try{n=JSON.stringify(e)??String(e)}catch{n=String(e)}return n.length<=t?n:n.slice(0,t-3)+"..."}function oy(e){const t=e.valid==null?"unknown":e.valid?"valid":"invalid",n=lr(e.schema),i=n.schema?n.unsupportedPaths.length>0:!1,s=n.schema?.properties??{},a=Do.filter(I=>I.key in s),o=new Set(Do.map(I=>I.key)),l=Object.keys(s).filter(I=>!o.has(I)).map(I=>({key:I,label:I.charAt(0).toUpperCase()+I.slice(1)})),d=[...a,...l],h=e.activeSection&&n.schema&&Se(n.schema)==="object"?n.schema.properties?.[e.activeSection]:void 0,p=e.activeSection?iy(e.activeSection,h):null,u=e.activeSection?sy({key:e.activeSection,schema:h,uiHints:e.uiHints}):[],y=e.formMode==="form"&&!!e.activeSection&&u.length>0,v=e.activeSubsection===Bo,$=e.searchQuery||v?null:e.activeSubsection??u[0]?.key??null,g=e.formMode==="form"?ay(e.originalValue,e.formValue):[],w=e.formMode==="raw"&&e.raw!==e.originalRaw,_=e.formMode==="form"?g.length>0:w,C=!!e.formValue&&!e.loading&&!!n.schema,L=e.connected&&!e.saving&&_&&(e.formMode==="raw"?!0:C),x=e.connected&&!e.applying&&!e.updating&&_&&(e.formMode==="raw"?!0:C),T=e.connected&&!e.applying&&!e.updating;return r`
    <div class="config-layout">
      <!-- Sidebar -->
      <aside class="config-sidebar">
        <div class="config-sidebar__header">
          <div class="config-sidebar__title">Settings</div>
          <span
            class="pill pill--sm ${t==="valid"?"pill--ok":t==="invalid"?"pill--danger":""}"
            >${t}</span
          >
        </div>

        <!-- Search -->
        <div class="config-search">
          <svg
            class="config-search__icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="11" cy="11" r="8"></circle>
            <path d="M21 21l-4.35-4.35"></path>
          </svg>
          <input
            type="text"
            class="config-search__input"
            placeholder="Search settings..."
            .value=${e.searchQuery}
            @input=${I=>e.onSearchChange(I.target.value)}
          />
          ${e.searchQuery?r`
                <button
                  class="config-search__clear"
                  @click=${()=>e.onSearchChange("")}
                >
                  ×
                </button>
              `:m}
        </div>

        <!-- Section nav -->
        <nav class="config-nav">
          <button
            class="config-nav__item ${e.activeSection===null?"active":""}"
            @click=${()=>e.onSectionChange(null)}
          >
            <span class="config-nav__icon">${as.all}</span>
            <span class="config-nav__label">All Settings</span>
          </button>
          ${d.map(I=>r`
              <button
                class="config-nav__item ${e.activeSection===I.key?"active":""}"
                @click=${()=>e.onSectionChange(I.key)}
              >
                <span class="config-nav__icon"
                  >${Uo(I.key)}</span
                >
                <span class="config-nav__label">${I.label}</span>
              </button>
            `)}
        </nav>

        <!-- Mode toggle at bottom -->
        <div class="config-sidebar__footer">
          <div class="config-mode-toggle">
            <button
              class="config-mode-toggle__btn ${e.formMode==="form"?"active":""}"
              ?disabled=${e.schemaLoading||!e.schema}
              @click=${()=>e.onFormModeChange("form")}
            >
              Form
            </button>
            <button
              class="config-mode-toggle__btn ${e.formMode==="raw"?"active":""}"
              @click=${()=>e.onFormModeChange("raw")}
            >
              Raw
            </button>
          </div>
        </div>
      </aside>

      <!-- Main content -->
      <main class="config-main">
        <!-- Action bar -->
        <div class="config-actions">
          <div class="config-actions__left">
            ${_?r`
                  <span class="config-changes-badge"
                    >${e.formMode==="raw"?"Unsaved changes":`${g.length} unsaved change${g.length!==1?"s":""}`}</span
                  >
                `:r`
                    <span class="config-status muted">No changes</span>
                  `}
          </div>
          <div class="config-actions__right">
            <button
              class="btn btn--sm"
              ?disabled=${e.loading}
              @click=${e.onReload}
            >
              ${e.loading?"Loading…":"Reload"}
            </button>
            <button
              class="btn btn--sm primary"
              ?disabled=${!L}
              @click=${e.onSave}
            >
              ${e.saving?"Saving…":"Save"}
            </button>
            <button
              class="btn btn--sm"
              ?disabled=${!x}
              @click=${e.onApply}
            >
              ${e.applying?"Applying…":"Apply"}
            </button>
            <button
              class="btn btn--sm"
              ?disabled=${!T}
              @click=${e.onUpdate}
            >
              ${e.updating?"Updating…":"Update"}
            </button>
          </div>
        </div>

        <!-- Diff panel (form mode only - raw mode doesn't have granular diff) -->
        ${_&&e.formMode==="form"?r`
              <details class="config-diff">
                <summary class="config-diff__summary">
                  <span
                    >View ${g.length} pending
                    change${g.length!==1?"s":""}</span
                  >
                  <svg
                    class="config-diff__chevron"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <polyline points="6 9 12 15 18 9"></polyline>
                  </svg>
                </summary>
                <div class="config-diff__content">
                  ${g.map(I=>r`
                      <div class="config-diff__item">
                        <div class="config-diff__path">${I.path}</div>
                        <div class="config-diff__values">
                          <span class="config-diff__from"
                            >${Ko(I.from)}</span
                          >
                          <span class="config-diff__arrow">→</span>
                          <span class="config-diff__to"
                            >${Ko(I.to)}</span
                          >
                        </div>
                      </div>
                    `)}
                </div>
              </details>
            `:m}
        ${p&&e.formMode==="form"?r`
              <div class="config-section-hero">
                <div class="config-section-hero__icon">
                  ${Uo(e.activeSection??"")}
                </div>
                <div class="config-section-hero__text">
                  <div class="config-section-hero__title">
                    ${p.label}
                  </div>
                  ${p.description?r`<div class="config-section-hero__desc">
                        ${p.description}
                      </div>`:m}
                </div>
              </div>
            `:m}
        ${y?r`
              <div class="config-subnav">
                <button
                  class="config-subnav__item ${$===null?"active":""}"
                  @click=${()=>e.onSubsectionChange(Bo)}
                >
                  All
                </button>
                ${u.map(I=>r`
                    <button
                      class="config-subnav__item ${$===I.key?"active":""}"
                      title=${I.description||I.label}
                      @click=${()=>e.onSubsectionChange(I.key)}
                    >
                      ${I.label}
                    </button>
                  `)}
              </div>
            `:m}

        <!-- Form content -->
        <div class="config-content">
          ${e.formMode==="form"?r`
                ${e.schemaLoading?r`
                        <div class="config-loading">
                          <div class="config-loading__spinner"></div>
                          <span>Loading schema…</span>
                        </div>
                      `:fv({schema:n.schema,uiHints:e.uiHints,value:e.formValue,disabled:e.loading||!e.formValue,unsupportedPaths:n.unsupportedPaths,onPatch:e.onFormPatch,searchQuery:e.searchQuery,activeSection:e.activeSection,activeSubsection:$})}
                ${i?r`
                        <div class="callout danger" style="margin-top: 12px">
                          Form view can't safely edit some fields. Use Raw to avoid losing config entries.
                        </div>
                      `:m}
              `:r`
                <label class="field config-raw-field">
                  <span>Raw JSON5</span>
                  <textarea
                    .value=${e.raw}
                    @input=${I=>e.onRawChange(I.target.value)}
                  ></textarea>
                </label>
              `}
        </div>

        ${e.issues.length>0?r`<div class="callout danger" style="margin-top: 12px;">
              <pre class="code-block">
${JSON.stringify(e.issues,null,2)}</pre
              >
            </div>`:m}
      </main>
    </div>
  `}function ly(e){const t=["last",...e.channels.filter(Boolean)],n=e.form.deliveryChannel?.trim();n&&!t.includes(n)&&t.push(n);const i=new Set;return t.filter(s=>i.has(s)?!1:(i.add(s),!0))}function ry(e,t){if(t==="last")return"last";const n=e.channelMeta?.find(i=>i.id===t);return n?.label?n.label:e.channelLabels?.[t]??t}function cy(e){const t=ly(e);return r`
    <section class="grid grid-cols-2">
      <div class="card">
        <div class="card-title">Scheduler</div>
        <div class="card-sub">Gateway-owned cron scheduler status.</div>
        <div class="stat-grid" style="margin-top: 16px;">
          <div class="stat">
            <div class="stat-label">Enabled</div>
            <div class="stat-value">
              ${e.status?e.status.enabled?"Yes":"No":"n/a"}
            </div>
          </div>
          <div class="stat">
            <div class="stat-label">Jobs</div>
            <div class="stat-value">${e.status?.jobs??"n/a"}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Next wake</div>
            <div class="stat-value">${Ps(e.status?.nextWakeAtMs??null)}</div>
          </div>
        </div>
        <div class="row" style="margin-top: 12px;">
          <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Refreshing…":"Refresh"}
          </button>
          ${e.error?r`<span class="muted">${e.error}</span>`:m}
        </div>
      </div>

      <div class="card">
        <div class="card-title">New Job</div>
        <div class="card-sub">Create a scheduled wakeup or agent run.</div>
        <div class="form-grid" style="margin-top: 16px;">
          <label class="field">
            <span>Name</span>
            <input
              .value=${e.form.name}
              @input=${n=>e.onFormChange({name:n.target.value})}
            />
          </label>
          <label class="field">
            <span>Description</span>
            <input
              .value=${e.form.description}
              @input=${n=>e.onFormChange({description:n.target.value})}
            />
          </label>
          <label class="field">
            <span>Agent ID</span>
            <input
              .value=${e.form.agentId}
              @input=${n=>e.onFormChange({agentId:n.target.value})}
              placeholder="default"
            />
          </label>
          <label class="field checkbox">
            <span>Enabled</span>
            <input
              type="checkbox"
              .checked=${e.form.enabled}
              @change=${n=>e.onFormChange({enabled:n.target.checked})}
            />
          </label>
          <label class="field">
            <span>Schedule</span>
            <select
              .value=${e.form.scheduleKind}
              @change=${n=>e.onFormChange({scheduleKind:n.target.value})}
            >
              <option value="every">Every</option>
              <option value="at">At</option>
              <option value="cron">Cron</option>
            </select>
          </label>
        </div>
        ${dy(e)}
        <div class="form-grid" style="margin-top: 12px;">
          <label class="field">
            <span>Session</span>
            <select
              .value=${e.form.sessionTarget}
              @change=${n=>e.onFormChange({sessionTarget:n.target.value})}
            >
              <option value="main">Main</option>
              <option value="isolated">Isolated</option>
            </select>
          </label>
          <label class="field">
            <span>Wake mode</span>
            <select
              .value=${e.form.wakeMode}
              @change=${n=>e.onFormChange({wakeMode:n.target.value})}
            >
              <option value="next-heartbeat">Next heartbeat</option>
              <option value="now">Now</option>
            </select>
          </label>
          <label class="field">
            <span>Payload</span>
            <select
              .value=${e.form.payloadKind}
              @change=${n=>e.onFormChange({payloadKind:n.target.value})}
            >
              <option value="systemEvent">System event</option>
              <option value="agentTurn">Agent turn</option>
            </select>
          </label>
        </div>
        <label class="field" style="margin-top: 12px;">
          <span>${e.form.payloadKind==="systemEvent"?"System text":"Agent message"}</span>
          <textarea
            .value=${e.form.payloadText}
            @input=${n=>e.onFormChange({payloadText:n.target.value})}
            rows="4"
          ></textarea>
        </label>
        ${e.form.payloadKind==="agentTurn"?r`
                <div class="form-grid" style="margin-top: 12px;">
                  <label class="field">
                    <span>Delivery</span>
                    <select
                      .value=${e.form.deliveryMode}
                      @change=${n=>e.onFormChange({deliveryMode:n.target.value})}
                    >
                      <option value="announce">Announce summary (default)</option>
                      <option value="none">None (internal)</option>
                    </select>
                  </label>
                  <label class="field">
                    <span>Timeout (seconds)</span>
                    <input
                      .value=${e.form.timeoutSeconds}
                      @input=${n=>e.onFormChange({timeoutSeconds:n.target.value})}
                    />
                  </label>
                  ${e.form.deliveryMode==="announce"?r`
                          <label class="field">
                            <span>Channel</span>
                            <select
                              .value=${e.form.deliveryChannel||"last"}
                              @change=${n=>e.onFormChange({deliveryChannel:n.target.value})}
                            >
                              ${t.map(n=>r`<option value=${n}>
                                    ${ry(e,n)}
                                  </option>`)}
                            </select>
                          </label>
                          <label class="field">
                            <span>To</span>
                            <input
                              .value=${e.form.deliveryTo}
                              @input=${n=>e.onFormChange({deliveryTo:n.target.value})}
                              placeholder="+1555… or chat id"
                            />
                          </label>
                        `:m}
                </div>
              `:m}
        <div class="row" style="margin-top: 14px;">
          <button class="btn primary" ?disabled=${e.busy} @click=${e.onAdd}>
            ${e.busy?"Saving…":"Add job"}
          </button>
        </div>
      </div>
    </section>

    <section class="card" style="margin-top: 18px;">
      <div class="card-title">Jobs</div>
      <div class="card-sub">All scheduled jobs stored in the gateway.</div>
      ${e.jobs.length===0?r`
              <div class="muted" style="margin-top: 12px">No jobs yet.</div>
            `:r`
            <div class="list" style="margin-top: 12px;">
              ${e.jobs.map(n=>uy(n,e))}
            </div>
          `}
    </section>

    <section class="card" style="margin-top: 18px;">
      <div class="card-title">Run history</div>
      <div class="card-sub">Latest runs for ${e.runsJobId??"(select a job)"}.</div>
      ${e.runsJobId==null?r`
              <div class="muted" style="margin-top: 12px">Select a job to inspect run history.</div>
            `:e.runs.length===0?r`
                <div class="muted" style="margin-top: 12px">No runs yet.</div>
              `:r`
              <div class="list" style="margin-top: 12px;">
                ${e.runs.map(n=>fy(n))}
              </div>
            `}
    </section>
  `}function dy(e){const t=e.form;return t.scheduleKind==="at"?r`
      <label class="field" style="margin-top: 12px;">
        <span>Run at</span>
        <input
          type="datetime-local"
          .value=${t.scheduleAt}
          @input=${n=>e.onFormChange({scheduleAt:n.target.value})}
        />
      </label>
    `:t.scheduleKind==="every"?r`
      <div class="form-grid" style="margin-top: 12px;">
        <label class="field">
          <span>Every</span>
          <input
            .value=${t.everyAmount}
            @input=${n=>e.onFormChange({everyAmount:n.target.value})}
          />
        </label>
        <label class="field">
          <span>Unit</span>
          <select
            .value=${t.everyUnit}
            @change=${n=>e.onFormChange({everyUnit:n.target.value})}
          >
            <option value="minutes">Minutes</option>
            <option value="hours">Hours</option>
            <option value="days">Days</option>
          </select>
        </label>
      </div>
    `:r`
    <div class="form-grid" style="margin-top: 12px;">
      <label class="field">
        <span>Expression</span>
        <input
          .value=${t.cronExpr}
          @input=${n=>e.onFormChange({cronExpr:n.target.value})}
        />
      </label>
      <label class="field">
        <span>Timezone (optional)</span>
        <input
          .value=${t.cronTz}
          @input=${n=>e.onFormChange({cronTz:n.target.value})}
        />
      </label>
    </div>
  `}function uy(e,t){const i=`list-item list-item-clickable${t.runsJobId===e.id?" list-item-selected":""}`;return r`
    <div class=${i} @click=${()=>t.onLoadRuns(e.id)}>
      <div class="list-main">
        <div class="list-title">${e.name}</div>
        <div class="list-sub">${er(e)}</div>
        <div class="muted">${tr(e)}</div>
        ${e.agentId?r`<div class="muted">Agent: ${e.agentId}</div>`:m}
        <div class="chip-row" style="margin-top: 6px;">
          <span class="chip">${e.enabled?"enabled":"disabled"}</span>
          <span class="chip">${e.sessionTarget}</span>
          <span class="chip">${e.wakeMode}</span>
        </div>
      </div>
      <div class="list-meta">
        <div>${Xl(e)}</div>
        <div class="row" style="justify-content: flex-end; margin-top: 8px;">
          <button
            class="btn"
            ?disabled=${t.busy}
            @click=${s=>{s.stopPropagation(),t.onToggle(e,!e.enabled)}}
          >
            ${e.enabled?"Disable":"Enable"}
          </button>
          <button
            class="btn"
            ?disabled=${t.busy}
            @click=${s=>{s.stopPropagation(),t.onRun(e)}}
          >
            Run
          </button>
          <button
            class="btn"
            ?disabled=${t.busy}
            @click=${s=>{s.stopPropagation(),t.onLoadRuns(e.id)}}
          >
            Runs
          </button>
          <button
            class="btn danger"
            ?disabled=${t.busy}
            @click=${s=>{s.stopPropagation(),t.onRemove(e)}}
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  `}function fy(e){return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${e.status}</div>
        <div class="list-sub">${e.summary??""}</div>
      </div>
      <div class="list-meta">
        <div>${Kt(e.ts)}</div>
        <div class="muted">${e.durationMs??0}ms</div>
        ${e.error?r`<div class="muted">${e.error}</div>`:m}
      </div>
    </div>
  `}function gy(e){const n=(e.status&&typeof e.status=="object"?e.status.securityAudit:null)?.summary??null,i=n?.critical??0,s=n?.warn??0,a=n?.info??0,o=i>0?"danger":s>0?"warn":"success",l=i>0?`${i} critical`:s>0?`${s} warnings`:"No critical issues";return r`
    <section class="grid grid-cols-2">
      <div class="card">
        <div class="row" style="justify-content: space-between;">
          <div>
            <div class="card-title">Snapshots</div>
            <div class="card-sub">Status, health, and heartbeat data.</div>
          </div>
          <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Refreshing…":"Refresh"}
          </button>
        </div>
        <div class="stack" style="margin-top: 12px;">
          <div>
            <div class="muted">Status</div>
            ${n?r`<div class="callout ${o}" style="margin-top: 8px;">
                  Security audit: ${l}${a>0?` · ${a} info`:""}. Run
                  <span class="mono">openclaw security audit --deep</span> for details.
                </div>`:m}
            <pre class="code-block">${JSON.stringify(e.status??{},null,2)}</pre>
          </div>
          <div>
            <div class="muted">Health</div>
            <pre class="code-block">${JSON.stringify(e.health??{},null,2)}</pre>
          </div>
          <div>
            <div class="muted">Last heartbeat</div>
            <pre class="code-block">${JSON.stringify(e.heartbeat??{},null,2)}</pre>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Manual RPC</div>
        <div class="card-sub">Send a raw gateway method with JSON params.</div>
        <div class="form-grid" style="margin-top: 16px;">
          <label class="field">
            <span>Method</span>
            <input
              .value=${e.callMethod}
              @input=${d=>e.onCallMethodChange(d.target.value)}
              placeholder="system-presence"
            />
          </label>
          <label class="field">
            <span>Params (JSON)</span>
            <textarea
              .value=${e.callParams}
              @input=${d=>e.onCallParamsChange(d.target.value)}
              rows="6"
            ></textarea>
          </label>
        </div>
        <div class="row" style="margin-top: 12px;">
          <button class="btn primary" @click=${e.onCall}>Call</button>
        </div>
        ${e.callError?r`<div class="callout danger" style="margin-top: 12px;">
              ${e.callError}
            </div>`:m}
        ${e.callResult?r`<pre class="code-block" style="margin-top: 12px;">${e.callResult}</pre>`:m}
      </div>
    </section>

    <section class="card" style="margin-top: 18px;">
      <div class="card-title">Models</div>
      <div class="card-sub">Catalog from models.list.</div>
      <pre class="code-block" style="margin-top: 12px;">${JSON.stringify(e.models??[],null,2)}</pre>
    </section>

    <section class="card" style="margin-top: 18px;">
      <div class="card-title">Event Log</div>
      <div class="card-sub">Latest gateway events.</div>
      ${e.eventLog.length===0?r`
              <div class="muted" style="margin-top: 12px">No events yet.</div>
            `:r`
            <div class="list" style="margin-top: 12px;">
              ${e.eventLog.map(d=>r`
                  <div class="list-item">
                    <div class="list-main">
                      <div class="list-title">${d.event}</div>
                      <div class="list-sub">${new Date(d.ts).toLocaleTimeString()}</div>
                    </div>
                    <div class="list-meta">
                      <pre class="code-block">${Tp(d.payload)}</pre>
                    </div>
                  </div>
                `)}
            </div>
          `}
    </section>
  `}function hy(e){const t=Math.max(0,e),n=Math.floor(t/1e3);if(n<60)return`${n}s`;const i=Math.floor(n/60);return i<60?`${i}m`:`${Math.floor(i/60)}h`}function Ge(e,t){return t?r`<div class="exec-approval-meta-row"><span>${e}</span><span>${t}</span></div>`:m}function py(e){const t=e.execApprovalQueue[0];if(!t)return m;const n=t.request,i=t.expiresAtMs-Date.now(),s=i>0?`expires in ${hy(i)}`:"expired",a=e.execApprovalQueue.length;return r`
    <div class="exec-approval-overlay" role="dialog" aria-live="polite">
      <div class="exec-approval-card">
        <div class="exec-approval-header">
          <div>
            <div class="exec-approval-title">Exec approval needed</div>
            <div class="exec-approval-sub">${s}</div>
          </div>
          ${a>1?r`<div class="exec-approval-queue">${a} pending</div>`:m}
        </div>
        <div class="exec-approval-command mono">${n.command}</div>
        <div class="exec-approval-meta">
          ${Ge("Host",n.host)}
          ${Ge("Agent",n.agentId)}
          ${Ge("Session",n.sessionKey)}
          ${Ge("CWD",n.cwd)}
          ${Ge("Resolved",n.resolvedPath)}
          ${Ge("Security",n.security)}
          ${Ge("Ask",n.ask)}
        </div>
        ${e.execApprovalError?r`<div class="exec-approval-error">${e.execApprovalError}</div>`:m}
        <div class="exec-approval-actions">
          <button
            class="btn primary"
            ?disabled=${e.execApprovalBusy}
            @click=${()=>e.handleExecApprovalDecision("allow-once")}
          >
            Allow once
          </button>
          <button
            class="btn"
            ?disabled=${e.execApprovalBusy}
            @click=${()=>e.handleExecApprovalDecision("allow-always")}
          >
            Always allow
          </button>
          <button
            class="btn danger"
            ?disabled=${e.execApprovalBusy}
            @click=${()=>e.handleExecApprovalDecision("deny")}
          >
            Deny
          </button>
        </div>
      </div>
    </div>
  `}function vy(e){const{pendingGatewayUrl:t}=e;return t?r`
    <div class="exec-approval-overlay" role="dialog" aria-modal="true" aria-live="polite">
      <div class="exec-approval-card">
        <div class="exec-approval-header">
          <div>
            <div class="exec-approval-title">Change Gateway URL</div>
            <div class="exec-approval-sub">This will reconnect to a different gateway server</div>
          </div>
        </div>
        <div class="exec-approval-command mono">${t}</div>
        <div class="callout danger" style="margin-top: 12px;">
          Only confirm if you trust this URL. Malicious URLs can compromise your system.
        </div>
        <div class="exec-approval-actions">
          <button
            class="btn primary"
            @click=${()=>e.handleGatewayUrlConfirm()}
          >
            Confirm
          </button>
          <button
            class="btn"
            @click=${()=>e.handleGatewayUrlCancel()}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  `:m}function my(e){return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Connected Instances</div>
          <div class="card-sub">Presence beacons from the gateway and clients.</div>
        </div>
        <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
          ${e.loading?"Loading…":"Refresh"}
        </button>
      </div>
      ${e.lastError?r`<div class="callout danger" style="margin-top: 12px;">
            ${e.lastError}
          </div>`:m}
      ${e.statusMessage?r`<div class="callout" style="margin-top: 12px;">
            ${e.statusMessage}
          </div>`:m}
      <div class="list" style="margin-top: 16px;">
        ${e.entries.length===0?r`
                <div class="muted">No instances reported yet.</div>
              `:e.entries.map(t=>by(t))}
      </div>
    </section>
  `}function by(e){const t=e.lastInputSeconds!=null?`${e.lastInputSeconds}s ago`:"n/a",n=e.mode??"unknown",i=Array.isArray(e.roles)?e.roles.filter(Boolean):[],s=Array.isArray(e.scopes)?e.scopes.filter(Boolean):[],a=s.length>0?s.length>3?`${s.length} scopes`:`scopes: ${s.join(", ")}`:null;return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${e.host??"unknown host"}</div>
        <div class="list-sub">${_p(e)}</div>
        <div class="chip-row">
          <span class="chip">${n}</span>
          ${i.map(o=>r`<span class="chip">${o}</span>`)}
          ${a?r`<span class="chip">${a}</span>`:m}
          ${e.platform?r`<span class="chip">${e.platform}</span>`:m}
          ${e.deviceFamily?r`<span class="chip">${e.deviceFamily}</span>`:m}
          ${e.modelIdentifier?r`<span class="chip">${e.modelIdentifier}</span>`:m}
          ${e.version?r`<span class="chip">${e.version}</span>`:m}
        </div>
      </div>
      <div class="list-meta">
        <div>${Cp(e)}</div>
        <div class="muted">Last input ${t}</div>
        <div class="muted">Reason ${e.reason??""}</div>
      </div>
    </div>
  `}const zo=["trace","debug","info","warn","error","fatal"];function yy(e){if(!e)return"";const t=new Date(e);return Number.isNaN(t.getTime())?e:t.toLocaleTimeString()}function wy(e,t){return t?[e.message,e.subsystem,e.raw].filter(Boolean).join(" ").toLowerCase().includes(t):!0}function $y(e){const t=e.filterText.trim().toLowerCase(),n=zo.some(a=>!e.levelFilters[a]),i=e.entries.filter(a=>a.level&&!e.levelFilters[a.level]?!1:wy(a,t)),s=t||n?"filtered":"visible";return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Logs</div>
          <div class="card-sub">Gateway file logs (JSONL).</div>
        </div>
        <div class="row" style="gap: 8px;">
          <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
            ${e.loading?"Loading…":"Refresh"}
          </button>
          <button
            class="btn"
            ?disabled=${i.length===0}
            @click=${()=>e.onExport(i.map(a=>a.raw),s)}
          >
            Export ${s}
          </button>
        </div>
      </div>

      <div class="filters" style="margin-top: 14px;">
        <label class="field" style="min-width: 220px;">
          <span>Filter</span>
          <input
            .value=${e.filterText}
            @input=${a=>e.onFilterTextChange(a.target.value)}
            placeholder="Search logs"
          />
        </label>
        <label class="field checkbox">
          <span>Auto-follow</span>
          <input
            type="checkbox"
            .checked=${e.autoFollow}
            @change=${a=>e.onToggleAutoFollow(a.target.checked)}
          />
        </label>
      </div>

      <div class="chip-row" style="margin-top: 12px;">
        ${zo.map(a=>r`
            <label class="chip log-chip ${a}">
              <input
                type="checkbox"
                .checked=${e.levelFilters[a]}
                @change=${o=>e.onLevelToggle(a,o.target.checked)}
              />
              <span>${a}</span>
            </label>
          `)}
      </div>

      ${e.file?r`<div class="muted" style="margin-top: 10px;">File: ${e.file}</div>`:m}
      ${e.truncated?r`
              <div class="callout" style="margin-top: 10px">Log output truncated; showing latest chunk.</div>
            `:m}
      ${e.error?r`<div class="callout danger" style="margin-top: 10px;">${e.error}</div>`:m}

      <div class="log-stream" style="margin-top: 12px;" @scroll=${e.onScroll}>
        ${i.length===0?r`
                <div class="muted" style="padding: 12px">No log entries.</div>
              `:i.map(a=>r`
                <div class="log-row">
                  <div class="log-time mono">${yy(a.time)}</div>
                  <div class="log-level ${a.level??""}">${a.level??""}</div>
                  <div class="log-subsystem mono">${a.subsystem??""}</div>
                  <div class="log-message mono">${a.message??a.raw}</div>
                </div>
              `)}
      </div>
    </section>
  `}function ky(e){const t=Ey(e),n=Py(e);return r`
    ${Ny(n)}
    ${Fy(t)}
    ${Ay(e)}
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Nodes</div>
          <div class="card-sub">Paired devices and live links.</div>
        </div>
        <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
          ${e.loading?"Loading…":"Refresh"}
        </button>
      </div>
      <div class="list" style="margin-top: 16px;">
        ${e.nodes.length===0?r`
                <div class="muted">No nodes found.</div>
              `:e.nodes.map(i=>Wy(i))}
      </div>
    </section>
  `}function Ay(e){const t=e.devicesList??{pending:[],paired:[]},n=Array.isArray(t.pending)?t.pending:[],i=Array.isArray(t.paired)?t.paired:[];return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Devices</div>
          <div class="card-sub">Pairing requests + role tokens.</div>
        </div>
        <button class="btn" ?disabled=${e.devicesLoading} @click=${e.onDevicesRefresh}>
          ${e.devicesLoading?"Loading…":"Refresh"}
        </button>
      </div>
      ${e.devicesError?r`<div class="callout danger" style="margin-top: 12px;">${e.devicesError}</div>`:m}
      <div class="list" style="margin-top: 16px;">
        ${n.length>0?r`
              <div class="muted" style="margin-bottom: 8px;">Pending</div>
              ${n.map(s=>Sy(s,e))}
            `:m}
        ${i.length>0?r`
              <div class="muted" style="margin-top: 12px; margin-bottom: 8px;">Paired</div>
              ${i.map(s=>xy(s,e))}
            `:m}
        ${n.length===0&&i.length===0?r`
                <div class="muted">No paired devices.</div>
              `:m}
      </div>
    </section>
  `}function Sy(e,t){const n=e.displayName?.trim()||e.deviceId,i=typeof e.ts=="number"?U(e.ts):"n/a",s=e.role?.trim()?`role: ${e.role}`:"role: -",a=e.isRepair?" · repair":"",o=e.remoteIp?` · ${e.remoteIp}`:"";return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${n}</div>
        <div class="list-sub">${e.deviceId}${o}</div>
        <div class="muted" style="margin-top: 6px;">
          ${s} · requested ${i}${a}
        </div>
      </div>
      <div class="list-meta">
        <div class="row" style="justify-content: flex-end; gap: 8px; flex-wrap: wrap;">
          <button class="btn btn--sm primary" @click=${()=>t.onDeviceApprove(e.requestId)}>
            Approve
          </button>
          <button class="btn btn--sm" @click=${()=>t.onDeviceReject(e.requestId)}>
            Reject
          </button>
        </div>
      </div>
    </div>
  `}function xy(e,t){const n=e.displayName?.trim()||e.deviceId,i=e.remoteIp?` · ${e.remoteIp}`:"",s=`roles: ${Mi(e.roles)}`,a=`scopes: ${Mi(e.scopes)}`,o=Array.isArray(e.tokens)?e.tokens:[];return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${n}</div>
        <div class="list-sub">${e.deviceId}${i}</div>
        <div class="muted" style="margin-top: 6px;">${s} · ${a}</div>
        ${o.length===0?r`
                <div class="muted" style="margin-top: 6px">Tokens: none</div>
              `:r`
              <div class="muted" style="margin-top: 10px;">Tokens</div>
              <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 6px;">
                ${o.map(l=>_y(e.deviceId,l,t))}
              </div>
            `}
      </div>
    </div>
  `}function _y(e,t,n){const i=t.revokedAtMs?"revoked":"active",s=`scopes: ${Mi(t.scopes)}`,a=U(t.rotatedAtMs??t.createdAtMs??t.lastUsedAtMs??null);return r`
    <div class="row" style="justify-content: space-between; gap: 8px;">
      <div class="list-sub">${t.role} · ${i} · ${s} · ${a}</div>
      <div class="row" style="justify-content: flex-end; gap: 6px; flex-wrap: wrap;">
        <button
          class="btn btn--sm"
          @click=${()=>n.onDeviceRotate(e,t.role,t.scopes)}
        >
          Rotate
        </button>
        ${t.revokedAtMs?m:r`
              <button
                class="btn btn--sm danger"
                @click=${()=>n.onDeviceRevoke(e,t.role)}
              >
                Revoke
              </button>
            `}
      </div>
    </div>
  `}const Fe="__defaults__",Ho=[{value:"deny",label:"Deny"},{value:"allowlist",label:"Allowlist"},{value:"full",label:"Full"}],Cy=[{value:"off",label:"Off"},{value:"on-miss",label:"On miss"},{value:"always",label:"Always"}];function Ey(e){const t=e.configForm,n=Hy(e.nodes),{defaultBinding:i,agents:s}=Gy(t),a=!!t,o=e.configSaving||e.configFormMode==="raw";return{ready:a,disabled:o,configDirty:e.configDirty,configLoading:e.configLoading,configSaving:e.configSaving,defaultBinding:i,agents:s,nodes:n,onBindDefault:e.onBindDefault,onBindAgent:e.onBindAgent,onSave:e.onSaveBindings,onLoadConfig:e.onLoadConfig,formMode:e.configFormMode}}function jo(e){return e==="allowlist"||e==="full"||e==="deny"?e:"deny"}function Ty(e){return e==="always"||e==="off"||e==="on-miss"?e:"on-miss"}function Ly(e){const t=e?.defaults??{};return{security:jo(t.security),ask:Ty(t.ask),askFallback:jo(t.askFallback??"deny"),autoAllowSkills:!!(t.autoAllowSkills??!1)}}function Iy(e){const t=e?.agents??{},n=Array.isArray(t.list)?t.list:[],i=[];return n.forEach(s=>{if(!s||typeof s!="object")return;const a=s,o=typeof a.id=="string"?a.id.trim():"";if(!o)return;const l=typeof a.name=="string"?a.name.trim():void 0,d=a.default===!0;i.push({id:o,name:l||void 0,isDefault:d})}),i}function Ry(e,t){const n=Iy(e),i=Object.keys(t?.agents??{}),s=new Map;n.forEach(o=>s.set(o.id,o)),i.forEach(o=>{s.has(o)||s.set(o,{id:o})});const a=Array.from(s.values());return a.length===0&&a.push({id:"main",isDefault:!0}),a.sort((o,l)=>{if(o.isDefault&&!l.isDefault)return-1;if(!o.isDefault&&l.isDefault)return 1;const d=o.name?.trim()?o.name:o.id,h=l.name?.trim()?l.name:l.id;return d.localeCompare(h)}),a}function My(e,t){return e===Fe?Fe:e&&t.some(n=>n.id===e)?e:Fe}function Py(e){const t=e.execApprovalsForm??e.execApprovalsSnapshot?.file??null,n=!!t,i=Ly(t),s=Ry(e.configForm,t),a=jy(e.nodes),o=e.execApprovalsTarget;let l=o==="node"&&e.execApprovalsTargetNodeId?e.execApprovalsTargetNodeId:null;o==="node"&&l&&!a.some(u=>u.id===l)&&(l=null);const d=My(e.execApprovalsSelectedAgent,s),h=d!==Fe?(t?.agents??{})[d]??null:null,p=Array.isArray(h?.allowlist)?h.allowlist??[]:[];return{ready:n,disabled:e.execApprovalsSaving||e.execApprovalsLoading,dirty:e.execApprovalsDirty,loading:e.execApprovalsLoading,saving:e.execApprovalsSaving,form:t,defaults:i,selectedScope:d,selectedAgent:h,agents:s,allowlist:p,target:o,targetNodeId:l,targetNodes:a,onSelectScope:e.onExecApprovalsSelectAgent,onSelectTarget:e.onExecApprovalsTargetChange,onPatch:e.onExecApprovalsPatch,onRemove:e.onExecApprovalsRemove,onLoad:e.onLoadExecApprovals,onSave:e.onSaveExecApprovals}}function Fy(e){const t=e.nodes.length>0,n=e.defaultBinding??"";return r`
    <section class="card">
      <div class="row" style="justify-content: space-between; align-items: center;">
        <div>
          <div class="card-title">Exec node binding</div>
          <div class="card-sub">
            Pin agents to a specific node when using <span class="mono">exec host=node</span>.
          </div>
        </div>
        <button
          class="btn"
          ?disabled=${e.disabled||!e.configDirty}
          @click=${e.onSave}
        >
          ${e.configSaving?"Saving…":"Save"}
        </button>
      </div>

      ${e.formMode==="raw"?r`
              <div class="callout warn" style="margin-top: 12px">
                Switch the Config tab to <strong>Form</strong> mode to edit bindings here.
              </div>
            `:m}

      ${e.ready?r`
            <div class="list" style="margin-top: 16px;">
              <div class="list-item">
                <div class="list-main">
                  <div class="list-title">Default binding</div>
                  <div class="list-sub">Used when agents do not override a node binding.</div>
                </div>
                <div class="list-meta">
                  <label class="field">
                    <span>Node</span>
                    <select
                      ?disabled=${e.disabled||!t}
                      @change=${i=>{const a=i.target.value.trim();e.onBindDefault(a||null)}}
                    >
                      <option value="" ?selected=${n===""}>Any node</option>
                      ${e.nodes.map(i=>r`<option
                            value=${i.id}
                            ?selected=${n===i.id}
                          >
                            ${i.label}
                          </option>`)}
                    </select>
                  </label>
                  ${t?m:r`
                          <div class="muted">No nodes with system.run available.</div>
                        `}
                </div>
              </div>

              ${e.agents.length===0?r`
                      <div class="muted">No agents found.</div>
                    `:e.agents.map(i=>zy(i,e))}
            </div>
          `:r`<div class="row" style="margin-top: 12px; gap: 12px;">
            <div class="muted">Load config to edit bindings.</div>
            <button class="btn" ?disabled=${e.configLoading} @click=${e.onLoadConfig}>
              ${e.configLoading?"Loading…":"Load config"}
            </button>
          </div>`}
    </section>
  `}function Ny(e){const t=e.ready,n=e.target!=="node"||!!e.targetNodeId;return r`
    <section class="card">
      <div class="row" style="justify-content: space-between; align-items: center;">
        <div>
          <div class="card-title">Exec approvals</div>
          <div class="card-sub">
            Allowlist and approval policy for <span class="mono">exec host=gateway/node</span>.
          </div>
        </div>
        <button
          class="btn"
          ?disabled=${e.disabled||!e.dirty||!n}
          @click=${e.onSave}
        >
          ${e.saving?"Saving…":"Save"}
        </button>
      </div>

      ${Oy(e)}

      ${t?r`
            ${Dy(e)}
            ${By(e)}
            ${e.selectedScope===Fe?m:Uy(e)}
          `:r`<div class="row" style="margin-top: 12px; gap: 12px;">
            <div class="muted">Load exec approvals to edit allowlists.</div>
            <button class="btn" ?disabled=${e.loading||!n} @click=${e.onLoad}>
              ${e.loading?"Loading…":"Load approvals"}
            </button>
          </div>`}
    </section>
  `}function Oy(e){const t=e.targetNodes.length>0,n=e.targetNodeId??"";return r`
    <div class="list" style="margin-top: 12px;">
      <div class="list-item">
        <div class="list-main">
          <div class="list-title">Target</div>
          <div class="list-sub">
            Gateway edits local approvals; node edits the selected node.
          </div>
        </div>
        <div class="list-meta">
          <label class="field">
            <span>Host</span>
            <select
              ?disabled=${e.disabled}
              @change=${i=>{if(i.target.value==="node"){const o=e.targetNodes[0]?.id??null;e.onSelectTarget("node",n||o)}else e.onSelectTarget("gateway",null)}}
            >
              <option value="gateway" ?selected=${e.target==="gateway"}>Gateway</option>
              <option value="node" ?selected=${e.target==="node"}>Node</option>
            </select>
          </label>
          ${e.target==="node"?r`
                <label class="field">
                  <span>Node</span>
                  <select
                    ?disabled=${e.disabled||!t}
                    @change=${i=>{const a=i.target.value.trim();e.onSelectTarget("node",a||null)}}
                  >
                    <option value="" ?selected=${n===""}>Select node</option>
                    ${e.targetNodes.map(i=>r`<option
                          value=${i.id}
                          ?selected=${n===i.id}
                        >
                          ${i.label}
                        </option>`)}
                  </select>
                </label>
              `:m}
        </div>
      </div>
      ${e.target==="node"&&!t?r`
              <div class="muted">No nodes advertise exec approvals yet.</div>
            `:m}
    </div>
  `}function Dy(e){return r`
    <div class="row" style="margin-top: 12px; gap: 8px; flex-wrap: wrap;">
      <span class="label">Scope</span>
      <div class="row" style="gap: 8px; flex-wrap: wrap;">
        <button
          class="btn btn--sm ${e.selectedScope===Fe?"active":""}"
          @click=${()=>e.onSelectScope(Fe)}
        >
          Defaults
        </button>
        ${e.agents.map(t=>{const n=t.name?.trim()?`${t.name} (${t.id})`:t.id;return r`
            <button
              class="btn btn--sm ${e.selectedScope===t.id?"active":""}"
              @click=${()=>e.onSelectScope(t.id)}
            >
              ${n}
            </button>
          `})}
      </div>
    </div>
  `}function By(e){const t=e.selectedScope===Fe,n=e.defaults,i=e.selectedAgent??{},s=t?["defaults"]:["agents",e.selectedScope],a=typeof i.security=="string"?i.security:void 0,o=typeof i.ask=="string"?i.ask:void 0,l=typeof i.askFallback=="string"?i.askFallback:void 0,d=t?n.security:a??"__default__",h=t?n.ask:o??"__default__",p=t?n.askFallback:l??"__default__",u=typeof i.autoAllowSkills=="boolean"?i.autoAllowSkills:void 0,y=u??n.autoAllowSkills,v=u==null;return r`
    <div class="list" style="margin-top: 16px;">
      <div class="list-item">
        <div class="list-main">
          <div class="list-title">Security</div>
          <div class="list-sub">
            ${t?"Default security mode.":`Default: ${n.security}.`}
          </div>
        </div>
        <div class="list-meta">
          <label class="field">
            <span>Mode</span>
            <select
              ?disabled=${e.disabled}
              @change=${$=>{const w=$.target.value;!t&&w==="__default__"?e.onRemove([...s,"security"]):e.onPatch([...s,"security"],w)}}
            >
              ${t?m:r`<option value="__default__" ?selected=${d==="__default__"}>
                    Use default (${n.security})
                  </option>`}
              ${Ho.map($=>r`<option
                    value=${$.value}
                    ?selected=${d===$.value}
                  >
                    ${$.label}
                  </option>`)}
            </select>
          </label>
        </div>
      </div>

      <div class="list-item">
        <div class="list-main">
          <div class="list-title">Ask</div>
          <div class="list-sub">
            ${t?"Default prompt policy.":`Default: ${n.ask}.`}
          </div>
        </div>
        <div class="list-meta">
          <label class="field">
            <span>Mode</span>
            <select
              ?disabled=${e.disabled}
              @change=${$=>{const w=$.target.value;!t&&w==="__default__"?e.onRemove([...s,"ask"]):e.onPatch([...s,"ask"],w)}}
            >
              ${t?m:r`<option value="__default__" ?selected=${h==="__default__"}>
                    Use default (${n.ask})
                  </option>`}
              ${Cy.map($=>r`<option
                    value=${$.value}
                    ?selected=${h===$.value}
                  >
                    ${$.label}
                  </option>`)}
            </select>
          </label>
        </div>
      </div>

      <div class="list-item">
        <div class="list-main">
          <div class="list-title">Ask fallback</div>
          <div class="list-sub">
            ${t?"Applied when the UI prompt is unavailable.":`Default: ${n.askFallback}.`}
          </div>
        </div>
        <div class="list-meta">
          <label class="field">
            <span>Fallback</span>
            <select
              ?disabled=${e.disabled}
              @change=${$=>{const w=$.target.value;!t&&w==="__default__"?e.onRemove([...s,"askFallback"]):e.onPatch([...s,"askFallback"],w)}}
            >
              ${t?m:r`<option value="__default__" ?selected=${p==="__default__"}>
                    Use default (${n.askFallback})
                  </option>`}
              ${Ho.map($=>r`<option
                    value=${$.value}
                    ?selected=${p===$.value}
                  >
                    ${$.label}
                  </option>`)}
            </select>
          </label>
        </div>
      </div>

      <div class="list-item">
        <div class="list-main">
          <div class="list-title">Auto-allow skill CLIs</div>
          <div class="list-sub">
            ${t?"Allow skill executables listed by the Gateway.":v?`Using default (${n.autoAllowSkills?"on":"off"}).`:`Override (${y?"on":"off"}).`}
          </div>
        </div>
        <div class="list-meta">
          <label class="field">
            <span>Enabled</span>
            <input
              type="checkbox"
              ?disabled=${e.disabled}
              .checked=${y}
              @change=${$=>{const g=$.target;e.onPatch([...s,"autoAllowSkills"],g.checked)}}
            />
          </label>
          ${!t&&!v?r`<button
                class="btn btn--sm"
                ?disabled=${e.disabled}
                @click=${()=>e.onRemove([...s,"autoAllowSkills"])}
              >
                Use default
              </button>`:m}
        </div>
      </div>
    </div>
  `}function Uy(e){const t=["agents",e.selectedScope,"allowlist"],n=e.allowlist;return r`
    <div class="row" style="margin-top: 18px; justify-content: space-between;">
      <div>
        <div class="card-title">Allowlist</div>
        <div class="card-sub">Case-insensitive glob patterns.</div>
      </div>
      <button
        class="btn btn--sm"
        ?disabled=${e.disabled}
        @click=${()=>{const i=[...n,{pattern:""}];e.onPatch(t,i)}}
      >
        Add pattern
      </button>
    </div>
    <div class="list" style="margin-top: 12px;">
      ${n.length===0?r`
              <div class="muted">No allowlist entries yet.</div>
            `:n.map((i,s)=>Ky(e,i,s))}
    </div>
  `}function Ky(e,t,n){const i=t.lastUsedAt?U(t.lastUsedAt):"never",s=t.lastUsedCommand?Pi(t.lastUsedCommand,120):null,a=t.lastResolvedPath?Pi(t.lastResolvedPath,120):null;return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${t.pattern?.trim()?t.pattern:"New pattern"}</div>
        <div class="list-sub">Last used: ${i}</div>
        ${s?r`<div class="list-sub mono">${s}</div>`:m}
        ${a?r`<div class="list-sub mono">${a}</div>`:m}
      </div>
      <div class="list-meta">
        <label class="field">
          <span>Pattern</span>
          <input
            type="text"
            .value=${t.pattern??""}
            ?disabled=${e.disabled}
            @input=${o=>{const l=o.target;e.onPatch(["agents",e.selectedScope,"allowlist",n,"pattern"],l.value)}}
          />
        </label>
        <button
          class="btn btn--sm danger"
          ?disabled=${e.disabled}
          @click=${()=>{if(e.allowlist.length<=1){e.onRemove(["agents",e.selectedScope,"allowlist"]);return}e.onRemove(["agents",e.selectedScope,"allowlist",n])}}
        >
          Remove
        </button>
      </div>
    </div>
  `}function zy(e,t){const n=e.binding??"__default__",i=e.name?.trim()?`${e.name} (${e.id})`:e.id,s=t.nodes.length>0;return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${i}</div>
        <div class="list-sub">
          ${e.isDefault?"default agent":"agent"} ·
          ${n==="__default__"?`uses default (${t.defaultBinding??"any"})`:`override: ${e.binding}`}
        </div>
      </div>
      <div class="list-meta">
        <label class="field">
          <span>Binding</span>
          <select
            ?disabled=${t.disabled||!s}
            @change=${a=>{const l=a.target.value.trim();t.onBindAgent(e.index,l==="__default__"?null:l)}}
          >
            <option value="__default__" ?selected=${n==="__default__"}>
              Use default
            </option>
            ${t.nodes.map(a=>r`<option
                  value=${a.id}
                  ?selected=${n===a.id}
                >
                  ${a.label}
                </option>`)}
          </select>
        </label>
      </div>
    </div>
  `}function Hy(e){const t=[];for(const n of e){if(!(Array.isArray(n.commands)?n.commands:[]).some(l=>String(l)==="system.run"))continue;const a=typeof n.nodeId=="string"?n.nodeId.trim():"";if(!a)continue;const o=typeof n.displayName=="string"&&n.displayName.trim()?n.displayName.trim():a;t.push({id:a,label:o===a?a:`${o} · ${a}`})}return t.sort((n,i)=>n.label.localeCompare(i.label)),t}function jy(e){const t=[];for(const n of e){if(!(Array.isArray(n.commands)?n.commands:[]).some(l=>String(l)==="system.execApprovals.get"||String(l)==="system.execApprovals.set"))continue;const a=typeof n.nodeId=="string"?n.nodeId.trim():"";if(!a)continue;const o=typeof n.displayName=="string"&&n.displayName.trim()?n.displayName.trim():a;t.push({id:a,label:o===a?a:`${o} · ${a}`})}return t.sort((n,i)=>n.label.localeCompare(i.label)),t}function Gy(e){const t={id:"main",name:void 0,index:0,isDefault:!0,binding:null};if(!e||typeof e!="object")return{defaultBinding:null,agents:[t]};const i=(e.tools??{}).exec??{},s=typeof i.node=="string"&&i.node.trim()?i.node.trim():null,a=e.agents??{},o=Array.isArray(a.list)?a.list:[];if(o.length===0)return{defaultBinding:s,agents:[t]};const l=[];return o.forEach((d,h)=>{if(!d||typeof d!="object")return;const p=d,u=typeof p.id=="string"?p.id.trim():"";if(!u)return;const y=typeof p.name=="string"?p.name.trim():void 0,v=p.default===!0,g=(p.tools??{}).exec??{},w=typeof g.node=="string"&&g.node.trim()?g.node.trim():null;l.push({id:u,name:y||void 0,index:h,isDefault:v,binding:w})}),l.length===0&&l.push(t),{defaultBinding:s,agents:l}}function Wy(e){const t=!!e.connected,n=!!e.paired,i=typeof e.displayName=="string"&&e.displayName.trim()||(typeof e.nodeId=="string"?e.nodeId:"unknown"),s=Array.isArray(e.caps)?e.caps:[],a=Array.isArray(e.commands)?e.commands:[];return r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">${i}</div>
        <div class="list-sub">
          ${typeof e.nodeId=="string"?e.nodeId:""}
          ${typeof e.remoteIp=="string"?` · ${e.remoteIp}`:""}
          ${typeof e.version=="string"?` · ${e.version}`:""}
        </div>
        <div class="chip-row" style="margin-top: 6px;">
          <span class="chip">${n?"paired":"unpaired"}</span>
          <span class="chip ${t?"chip-ok":"chip-warn"}">
            ${t?"connected":"offline"}
          </span>
          ${s.slice(0,12).map(o=>r`<span class="chip">${String(o)}</span>`)}
          ${a.slice(0,8).map(o=>r`<span class="chip">${String(o)}</span>`)}
        </div>
      </div>
    </div>
  `}function qy(e){const t=e.hello?.snapshot,n=t?.uptimeMs?ul(t.uptimeMs):"n/a",i=t?.policy?.tickIntervalMs?`${t.policy.tickIntervalMs}ms`:"n/a",s=(()=>{if(e.connected||!e.lastError)return null;const o=e.lastError.toLowerCase();if(!(o.includes("unauthorized")||o.includes("connect failed")))return null;const d=!!e.settings.token.trim(),h=!!e.password.trim();return!d&&!h?r`
        <div class="muted" style="margin-top: 8px">
          This gateway requires auth. Add a token or password, then click Connect.
          <div style="margin-top: 6px">
            <span class="mono">openclaw dashboard --no-open</span> → tokenized URL<br />
            <span class="mono">openclaw doctor --generate-gateway-token</span> → set token
          </div>
          <div style="margin-top: 6px">
            <a
              class="session-link"
              href="https://docs.openclaw.ai/web/dashboard"
              target="_blank"
              rel="noreferrer"
              title="Control UI auth docs (opens in new tab)"
              >Docs: Control UI auth</a
            >
          </div>
        </div>
      `:r`
      <div class="muted" style="margin-top: 8px">
        Auth failed. Re-copy a tokenized URL with
        <span class="mono">openclaw dashboard --no-open</span>, or update the token, then click Connect.
        <div style="margin-top: 6px">
          <a
            class="session-link"
            href="https://docs.openclaw.ai/web/dashboard"
            target="_blank"
            rel="noreferrer"
            title="Control UI auth docs (opens in new tab)"
            >Docs: Control UI auth</a
          >
        </div>
      </div>
    `})(),a=(()=>{if(e.connected||!e.lastError||(typeof window<"u"?window.isSecureContext:!0))return null;const l=e.lastError.toLowerCase();return!l.includes("secure context")&&!l.includes("device identity required")?null:r`
      <div class="muted" style="margin-top: 8px">
        This page is HTTP, so the browser blocks device identity. Use HTTPS (Tailscale Serve) or open
        <span class="mono">http://127.0.0.1:18789</span> on the gateway host.
        <div style="margin-top: 6px">
          If you must stay on HTTP, set
          <span class="mono">gateway.controlUi.allowInsecureAuth: true</span> (token-only).
        </div>
        <div style="margin-top: 6px">
          <a
            class="session-link"
            href="https://docs.openclaw.ai/gateway/tailscale"
            target="_blank"
            rel="noreferrer"
            title="Tailscale Serve docs (opens in new tab)"
            >Docs: Tailscale Serve</a
          >
          <span class="muted"> · </span>
          <a
            class="session-link"
            href="https://docs.openclaw.ai/web/control-ui#insecure-http"
            target="_blank"
            rel="noreferrer"
            title="Insecure HTTP docs (opens in new tab)"
            >Docs: Insecure HTTP</a
          >
        </div>
      </div>
    `})();return r`
    <section class="grid grid-cols-2">
      <div class="card">
        <div class="card-title">Gateway Access</div>
        <div class="card-sub">Where the dashboard connects and how it authenticates.</div>
        <div class="form-grid" style="margin-top: 16px;">
          <label class="field">
            <span>WebSocket URL</span>
            <input
              .value=${e.settings.gatewayUrl}
              @input=${o=>{const l=o.target.value;e.onSettingsChange({...e.settings,gatewayUrl:l})}}
              placeholder="ws://100.x.y.z:18789"
            />
          </label>
          <label class="field">
            <span>Gateway Token</span>
            <input
              .value=${e.settings.token}
              @input=${o=>{const l=o.target.value;e.onSettingsChange({...e.settings,token:l})}}
              placeholder="OPENCLAW_GATEWAY_TOKEN"
            />
          </label>
          <label class="field">
            <span>Password (not stored)</span>
            <input
              type="password"
              .value=${e.password}
              @input=${o=>{const l=o.target.value;e.onPasswordChange(l)}}
              placeholder="system or shared password"
            />
          </label>
          <label class="field">
            <span>Default Session Key</span>
            <input
              .value=${e.settings.sessionKey}
              @input=${o=>{const l=o.target.value;e.onSessionKeyChange(l)}}
            />
          </label>
        </div>
        <div class="row" style="margin-top: 14px;">
          <button class="btn" @click=${()=>e.onConnect()}>Connect</button>
          <button class="btn" @click=${()=>e.onRefresh()}>Refresh</button>
          <span class="muted">Click Connect to apply connection changes.</span>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Snapshot</div>
        <div class="card-sub">Latest gateway handshake information.</div>
        <div class="stat-grid" style="margin-top: 16px;">
          <div class="stat">
            <div class="stat-label">Status</div>
            <div class="stat-value ${e.connected?"ok":"warn"}">
              ${e.connected?"Connected":"Disconnected"}
            </div>
          </div>
          <div class="stat">
            <div class="stat-label">Uptime</div>
            <div class="stat-value">${n}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Tick Interval</div>
            <div class="stat-value">${i}</div>
          </div>
          <div class="stat">
            <div class="stat-label">Last Channels Refresh</div>
            <div class="stat-value">
              ${e.lastChannelsRefresh?U(e.lastChannelsRefresh):"n/a"}
            </div>
          </div>
        </div>
        ${e.lastError?r`<div class="callout danger" style="margin-top: 14px;">
              <div>${e.lastError}</div>
              ${s??""}
              ${a??""}
            </div>`:r`
                <div class="callout" style="margin-top: 14px">
                  Use Channels to link WhatsApp, Telegram, Discord, Signal, or iMessage.
                </div>
              `}
      </div>
    </section>

    <section class="grid grid-cols-3" style="margin-top: 18px;">
      <div class="card stat-card">
        <div class="stat-label">Instances</div>
        <div class="stat-value">${e.presenceCount}</div>
        <div class="muted">Presence beacons in the last 5 minutes.</div>
      </div>
      <div class="card stat-card">
        <div class="stat-label">Sessions</div>
        <div class="stat-value">${e.sessionsCount??"n/a"}</div>
        <div class="muted">Recent session keys tracked by the gateway.</div>
      </div>
      <div class="card stat-card">
        <div class="stat-label">Cron</div>
        <div class="stat-value">
          ${e.cronEnabled==null?"n/a":e.cronEnabled?"Enabled":"Disabled"}
        </div>
        <div class="muted">Next wake ${Ps(e.cronNext)}</div>
      </div>
    </section>

    <section class="card" style="margin-top: 18px;">
      <div class="card-title">Notes</div>
      <div class="card-sub">Quick reminders for remote control setups.</div>
      <div class="note-grid" style="margin-top: 14px;">
        <div>
          <div class="note-title">Tailscale serve</div>
          <div class="muted">
            Prefer serve mode to keep the gateway on loopback with tailnet auth.
          </div>
        </div>
        <div>
          <div class="note-title">Session hygiene</div>
          <div class="muted">Use /new or sessions.patch to reset context.</div>
        </div>
        <div>
          <div class="note-title">Cron reminders</div>
          <div class="muted">Use isolated sessions for recurring runs.</div>
        </div>
      </div>
    </section>
  `}const Vy=["","off","minimal","low","medium","high"],Yy=["","off","on"],Qy=[{value:"",label:"inherit"},{value:"off",label:"off (explicit)"},{value:"on",label:"on"}],Jy=["","off","on","stream"];function Zy(e){if(!e)return"";const t=e.trim().toLowerCase();return t==="z.ai"||t==="z-ai"?"zai":t}function Dr(e){return Zy(e)==="zai"}function Xy(e){return Dr(e)?Yy:Vy}function e0(e,t){return!t||!e||e==="off"?e:"on"}function t0(e,t){return e?t&&e==="on"?"low":e:null}function n0(e){const t=e.result?.sessions??[];return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Sessions</div>
          <div class="card-sub">Active session keys and per-session overrides.</div>
        </div>
        <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
          ${e.loading?"Loading…":"Refresh"}
        </button>
      </div>

      <div class="filters" style="margin-top: 14px;">
        <label class="field">
          <span>Active within (minutes)</span>
          <input
            .value=${e.activeMinutes}
            @input=${n=>e.onFiltersChange({activeMinutes:n.target.value,limit:e.limit,includeGlobal:e.includeGlobal,includeUnknown:e.includeUnknown})}
          />
        </label>
        <label class="field">
          <span>Limit</span>
          <input
            .value=${e.limit}
            @input=${n=>e.onFiltersChange({activeMinutes:e.activeMinutes,limit:n.target.value,includeGlobal:e.includeGlobal,includeUnknown:e.includeUnknown})}
          />
        </label>
        <label class="field checkbox">
          <span>Include global</span>
          <input
            type="checkbox"
            .checked=${e.includeGlobal}
            @change=${n=>e.onFiltersChange({activeMinutes:e.activeMinutes,limit:e.limit,includeGlobal:n.target.checked,includeUnknown:e.includeUnknown})}
          />
        </label>
        <label class="field checkbox">
          <span>Include unknown</span>
          <input
            type="checkbox"
            .checked=${e.includeUnknown}
            @change=${n=>e.onFiltersChange({activeMinutes:e.activeMinutes,limit:e.limit,includeGlobal:e.includeGlobal,includeUnknown:n.target.checked})}
          />
        </label>
      </div>

      ${e.error?r`<div class="callout danger" style="margin-top: 12px;">${e.error}</div>`:m}

      <div class="muted" style="margin-top: 12px;">
        ${e.result?`Store: ${e.result.path}`:""}
      </div>

      <div class="table" style="margin-top: 16px;">
        <div class="table-head">
          <div>Key</div>
          <div>Label</div>
          <div>Kind</div>
          <div>Updated</div>
          <div>Tokens</div>
          <div>Thinking</div>
          <div>Verbose</div>
          <div>Reasoning</div>
          <div>Actions</div>
        </div>
        ${t.length===0?r`
                <div class="muted">No sessions found.</div>
              `:t.map(n=>i0(n,e.basePath,e.onPatch,e.onDelete,e.loading))}
      </div>
    </section>
  `}function i0(e,t,n,i,s){const a=e.updatedAt?U(e.updatedAt):"n/a",o=e.thinkingLevel??"",l=Dr(e.modelProvider),d=e0(o,l),h=Xy(e.modelProvider),p=e.verboseLevel??"",u=e.reasoningLevel??"",y=e.displayName??e.key,v=e.kind!=="global",$=v?`${Cs("chat",t)}?session=${encodeURIComponent(e.key)}`:null;return r`
    <div class="table-row">
      <div class="mono">${v?r`<a href=${$} class="session-link">${y}</a>`:y}</div>
      <div>
        <input
          .value=${e.label??""}
          ?disabled=${s}
          placeholder="(optional)"
          @change=${g=>{const w=g.target.value.trim();n(e.key,{label:w||null})}}
        />
      </div>
      <div>${e.kind}</div>
      <div>${a}</div>
      <div>${Ep(e)}</div>
      <div>
        <select
          .value=${d}
          ?disabled=${s}
          @change=${g=>{const w=g.target.value;n(e.key,{thinkingLevel:t0(w,l)})}}
        >
          ${h.map(g=>r`<option value=${g}>${g||"inherit"}</option>`)}
        </select>
      </div>
      <div>
        <select
          .value=${p}
          ?disabled=${s}
          @change=${g=>{const w=g.target.value;n(e.key,{verboseLevel:w||null})}}
        >
          ${Qy.map(g=>r`<option value=${g.value}>${g.label}</option>`)}
        </select>
      </div>
      <div>
        <select
          .value=${u}
          ?disabled=${s}
          @change=${g=>{const w=g.target.value;n(e.key,{reasoningLevel:w||null})}}
        >
          ${Jy.map(g=>r`<option value=${g}>${g||"inherit"}</option>`)}
        </select>
      </div>
      <div>
        <button class="btn danger" ?disabled=${s} @click=${()=>i(e.key)}>
          Delete
        </button>
      </div>
    </div>
  `}const mn=[{id:"workspace",label:"Workspace Skills",sources:["openclaw-workspace"]},{id:"built-in",label:"Built-in Skills",sources:["openclaw-bundled"]},{id:"installed",label:"Installed Skills",sources:["openclaw-managed"]},{id:"extra",label:"Extra Skills",sources:["openclaw-extra"]}];function s0(e){const t=new Map;for(const a of mn)t.set(a.id,{id:a.id,label:a.label,skills:[]});const n=mn.find(a=>a.id==="built-in"),i={id:"other",label:"Other Skills",skills:[]};for(const a of e){const o=a.bundled?n:mn.find(l=>l.sources.includes(a.source));o?t.get(o.id)?.skills.push(a):i.skills.push(a)}const s=mn.map(a=>t.get(a.id)).filter(a=>!!(a&&a.skills.length>0));return i.skills.length>0&&s.push(i),s}function a0(e){const t=e.report?.skills??[],n=e.filter.trim().toLowerCase(),i=n?t.filter(a=>[a.name,a.description,a.source].join(" ").toLowerCase().includes(n)):t,s=s0(i);return r`
    <section class="card">
      <div class="row" style="justify-content: space-between;">
        <div>
          <div class="card-title">Skills</div>
          <div class="card-sub">Bundled, managed, and workspace skills.</div>
        </div>
        <button class="btn" ?disabled=${e.loading} @click=${e.onRefresh}>
          ${e.loading?"Loading…":"Refresh"}
        </button>
      </div>

      <div class="filters" style="margin-top: 14px;">
        <label class="field" style="flex: 1;">
          <span>Filter</span>
          <input
            .value=${e.filter}
            @input=${a=>e.onFilterChange(a.target.value)}
            placeholder="Search skills"
          />
        </label>
        <div class="muted">${i.length} shown</div>
      </div>

      ${e.error?r`<div class="callout danger" style="margin-top: 12px;">${e.error}</div>`:m}

      ${i.length===0?r`
              <div class="muted" style="margin-top: 16px">No skills found.</div>
            `:r`
            <div class="agent-skills-groups" style="margin-top: 16px;">
              ${s.map(a=>{const o=a.id==="workspace"||a.id==="built-in";return r`
                  <details class="agent-skills-group" ?open=${!o}>
                    <summary class="agent-skills-header">
                      <span>${a.label}</span>
                      <span class="muted">${a.skills.length}</span>
                    </summary>
                    <div class="list skills-grid">
                      ${a.skills.map(l=>o0(l,e))}
                    </div>
                  </details>
                `})}
            </div>
          `}
    </section>
  `}function o0(e,t){const n=t.busyKey===e.skillKey,i=t.edits[e.skillKey]??"",s=t.messages[e.skillKey]??null,a=e.install.length>0&&e.missing.bins.length>0,o=!!(e.bundled&&e.source!=="openclaw-bundled"),l=[...e.missing.bins.map(h=>`bin:${h}`),...e.missing.env.map(h=>`env:${h}`),...e.missing.config.map(h=>`config:${h}`),...e.missing.os.map(h=>`os:${h}`)],d=[];return e.disabled&&d.push("disabled"),e.blockedByAllowlist&&d.push("blocked by allowlist"),r`
    <div class="list-item">
      <div class="list-main">
        <div class="list-title">
          ${e.emoji?`${e.emoji} `:""}${e.name}
        </div>
        <div class="list-sub">${Pi(e.description,140)}</div>
        <div class="chip-row" style="margin-top: 6px;">
          <span class="chip">${e.source}</span>
          ${o?r`
                  <span class="chip">bundled</span>
                `:m}
          <span class="chip ${e.eligible?"chip-ok":"chip-warn"}">
            ${e.eligible?"eligible":"blocked"}
          </span>
          ${e.disabled?r`
                  <span class="chip chip-warn">disabled</span>
                `:m}
        </div>
        ${l.length>0?r`
              <div class="muted" style="margin-top: 6px;">
                Missing: ${l.join(", ")}
              </div>
            `:m}
        ${d.length>0?r`
              <div class="muted" style="margin-top: 6px;">
                Reason: ${d.join(", ")}
              </div>
            `:m}
      </div>
      <div class="list-meta">
        <div class="row" style="justify-content: flex-end; flex-wrap: wrap;">
          <button
            class="btn"
            ?disabled=${n}
            @click=${()=>t.onToggle(e.skillKey,e.disabled)}
          >
            ${e.disabled?"Enable":"Disable"}
          </button>
          ${a?r`<button
                class="btn"
                ?disabled=${n}
                @click=${()=>t.onInstall(e.skillKey,e.name,e.install[0].id)}
              >
                ${n?"Installing…":e.install[0].label}
              </button>`:m}
        </div>
        ${s?r`<div
              class="muted"
              style="margin-top: 8px; color: ${s.kind==="error"?"var(--danger-color, #d14343)":"var(--success-color, #0a7f5a)"};"
            >
              ${s.message}
            </div>`:m}
        ${e.primaryEnv?r`
              <div class="field" style="margin-top: 10px;">
                <span>API key</span>
                <input
                  type="password"
                  .value=${i}
                  @input=${h=>t.onEdit(e.skillKey,h.target.value)}
                />
              </div>
              <button
                class="btn primary"
                style="margin-top: 8px;"
                ?disabled=${n}
                @click=${()=>t.onSaveKey(e.skillKey)}
              >
                Save key
              </button>
            `:m}
      </div>
    </div>
  `}const l0=/^data:/i,r0=/^https?:\/\//i;function c0(e){const t=e.agentsList?.agents??[],i=ll(e.sessionKey)?.agentId??e.agentsList?.defaultId??"main",a=t.find(l=>l.id===i)?.identity,o=a?.avatarUrl??a?.avatar;if(o)return l0.test(o)||r0.test(o)?o:a?.avatarUrl}function d0(e){const t=e.presenceEntries.length,n=e.sessionsResult?.count??null,i=e.cronStatus?.nextWakeAtMs??null,s=e.connected?null:"Disconnected from gateway.",a=e.tab==="chat",o=a&&(e.settings.chatFocusMode||e.onboarding),l=e.onboarding?!1:e.settings.chatShowThinking,d=c0(e),h=e.chatAvatarUrl??d??null,p=Yt(e.basePath),u=p?`${p}/favicon.svg`:"/favicon.svg",y=e.configForm??e.configSnapshot?.config,v=e.agentsSelectedId??e.agentsList?.defaultId??e.agentsList?.agents?.[0]?.id??null,$=g=>{const _=(e.configForm??e.configSnapshot?.config)?.agents?.list,C=Array.isArray(_)?_:[];let L=C.findIndex(x=>x&&typeof x=="object"&&"id"in x&&x.id===g);if(L<0){const x=[...C,{id:g}];q(e,["agents","list"],x),L=x.length-1}return L};return r`
    <div class="shell ${a?"shell--chat":""} ${o?"shell--chat-focus":""} ${e.settings.navCollapsed?"shell--nav-collapsed":""} ${e.onboarding?"shell--onboarding":""}">
      <header class="topbar">
        <div class="topbar-left">
          <button
            class="nav-collapse-toggle"
            @click=${()=>e.applySettings({...e.settings,navCollapsed:!e.settings.navCollapsed})}
            title="${e.settings.navCollapsed?"Expand sidebar":"Collapse sidebar"}"
            aria-label="${e.settings.navCollapsed?"Expand sidebar":"Collapse sidebar"}"
          >
            <span class="nav-collapse-toggle__icon">${J.menu}</span>
          </button>
          <div class="brand">
            <div class="brand-logo">
              <img src="${u}" alt="OpenClaw" />
            </div>
            <div class="brand-text">
              <div class="brand-title">OPENCLAW</div>
              <div class="brand-sub">Gateway Dashboard</div>
            </div>
          </div>
        </div>
        <div class="topbar-status">
          <div class="pill">
            <span class="statusDot ${e.connected?"ok":""}"></span>
            <span>Health</span>
            <span class="mono">${e.connected?"OK":"Offline"}</span>
          </div>
          ${pp(e)}
        </div>
      </header>
      <aside class="nav ${e.settings.navCollapsed?"nav--collapsed":""}">
        ${Kg.map(g=>{const w=e.settings.navGroupsCollapsed[g.label]??!1,_=g.tabs.some(C=>C===e.tab);return r`
            <div class="nav-group ${w&&!_?"nav-group--collapsed":""}">
              <button
                class="nav-label"
                @click=${()=>{const C={...e.settings.navGroupsCollapsed};C[g.label]=!w,e.applySettings({...e.settings,navGroupsCollapsed:C})}}
                aria-expanded=${!w}
              >
                <span class="nav-label__text">${g.label}</span>
                <span class="nav-label__chevron">${w?"+":"−"}</span>
              </button>
              <div class="nav-group__items">
                ${g.tabs.map(C=>dp(e,C))}
              </div>
            </div>
          `})}
        <div class="nav-group nav-group--links">
          <div class="nav-label nav-label--static">
            <span class="nav-label__text">Resources</span>
          </div>
          <div class="nav-group__items">
            <a
              class="nav-item nav-item--external"
              href="https://docs.openclaw.ai"
              target="_blank"
              rel="noreferrer"
              title="Docs (opens in new tab)"
            >
              <span class="nav-item__icon" aria-hidden="true">${J.book}</span>
              <span class="nav-item__text">Docs</span>
            </a>
          </div>
        </div>
      </aside>
      <main class="content ${a?"content--chat":""}">
        <section class="content-header">
          <div>
            <div class="page-title">${Bi(e.tab)}</div>
            <div class="page-sub">${jg(e.tab)}</div>
          </div>
          <div class="page-meta">
            ${e.lastError?r`<div class="pill danger">${e.lastError}</div>`:m}
            ${a?up(e):m}
          </div>
        </section>

        ${e.tab==="overview"?qy({connected:e.connected,hello:e.hello,settings:e.settings,password:e.password,lastError:e.lastError,presenceCount:t,sessionsCount:n,cronEnabled:e.cronStatus?.enabled??null,cronNext:i,lastChannelsRefresh:e.channelsLastSuccess,onSettingsChange:g=>e.applySettings(g),onPasswordChange:g=>e.password=g,onSessionKeyChange:g=>{e.sessionKey=g,e.chatMessage="",e.resetToolStream(),e.applySettings({...e.settings,sessionKey:g,lastActiveSessionKey:g}),e.loadAssistantIdentity()},onConnect:()=>e.connect(),onRefresh:()=>e.loadOverview()}):m}

        ${e.tab==="channels"?Mv({connected:e.connected,loading:e.channelsLoading,snapshot:e.channelsSnapshot,lastError:e.channelsError,lastSuccessAt:e.channelsLastSuccess,whatsappMessage:e.whatsappLoginMessage,whatsappQrDataUrl:e.whatsappLoginQrDataUrl,whatsappConnected:e.whatsappLoginConnected,whatsappBusy:e.whatsappBusy,configSchema:e.configSchema,configSchemaLoading:e.configSchemaLoading,configForm:e.configForm,configUiHints:e.configUiHints,configSaving:e.configSaving,configFormDirty:e.configFormDirty,nostrProfileFormState:e.nostrProfileFormState,nostrProfileAccountId:e.nostrProfileAccountId,onRefresh:g=>oe(e,g),onWhatsAppStart:g=>e.handleWhatsAppStart(g),onWhatsAppWait:()=>e.handleWhatsAppWait(),onWhatsAppLogout:()=>e.handleWhatsAppLogout(),onConfigPatch:(g,w)=>q(e,g,w),onConfigSave:()=>e.handleChannelConfigSave(),onConfigReload:()=>e.handleChannelConfigReload(),onNostrProfileEdit:(g,w)=>e.handleNostrProfileEdit(g,w),onNostrProfileCancel:()=>e.handleNostrProfileCancel(),onNostrProfileFieldChange:(g,w)=>e.handleNostrProfileFieldChange(g,w),onNostrProfileSave:()=>e.handleNostrProfileSave(),onNostrProfileImport:()=>e.handleNostrProfileImport(),onNostrProfileToggleAdvanced:()=>e.handleNostrProfileToggleAdvanced()}):m}

        ${e.tab==="instances"?my({loading:e.presenceLoading,entries:e.presenceEntries,lastError:e.presenceError,statusMessage:e.presenceStatus,onRefresh:()=>_s(e)}):m}

        ${e.tab==="sessions"?n0({loading:e.sessionsLoading,result:e.sessionsResult,error:e.sessionsError,activeMinutes:e.sessionsFilterActive,limit:e.sessionsFilterLimit,includeGlobal:e.sessionsIncludeGlobal,includeUnknown:e.sessionsIncludeUnknown,basePath:e.basePath,onFiltersChange:g=>{e.sessionsFilterActive=g.activeMinutes,e.sessionsFilterLimit=g.limit,e.sessionsIncludeGlobal=g.includeGlobal,e.sessionsIncludeUnknown=g.includeUnknown},onRefresh:()=>nt(e),onPatch:(g,w)=>Fg(e,g,w),onDelete:g=>Ng(e,g)}):m}

        ${e.tab==="cron"?cy({loading:e.cronLoading,status:e.cronStatus,jobs:e.cronJobs,error:e.cronError,busy:e.cronBusy,form:e.cronForm,channels:e.channelsSnapshot?.channelMeta?.length?e.channelsSnapshot.channelMeta.map(g=>g.id):e.channelsSnapshot?.channelOrder??[],channelLabels:e.channelsSnapshot?.channelLabels??{},channelMeta:e.channelsSnapshot?.channelMeta??[],runsJobId:e.cronRunsJobId,runs:e.cronRuns,onFormChange:g=>e.cronForm={...e.cronForm,...g},onRefresh:()=>e.loadCron(),onAdd:()=>Vf(e),onToggle:(g,w)=>Yf(e,g,w),onRun:g=>Qf(e,g),onRemove:g=>Jf(e,g),onLoadRuns:g=>gl(e,g)}):m}

        ${e.tab==="agents"?Dp({loading:e.agentsLoading,error:e.agentsError,agentsList:e.agentsList,selectedAgentId:v,activePanel:e.agentsPanel,configForm:y,configLoading:e.configLoading,configSaving:e.configSaving,configDirty:e.configFormDirty,channelsLoading:e.channelsLoading,channelsError:e.channelsError,channelsSnapshot:e.channelsSnapshot,channelsLastSuccess:e.channelsLastSuccess,cronLoading:e.cronLoading,cronStatus:e.cronStatus,cronJobs:e.cronJobs,cronError:e.cronError,agentFilesLoading:e.agentFilesLoading,agentFilesError:e.agentFilesError,agentFilesList:e.agentFilesList,agentFileActive:e.agentFileActive,agentFileContents:e.agentFileContents,agentFileDrafts:e.agentFileDrafts,agentFileSaving:e.agentFileSaving,agentIdentityLoading:e.agentIdentityLoading,agentIdentityError:e.agentIdentityError,agentIdentityById:e.agentIdentityById,agentSkillsLoading:e.agentSkillsLoading,agentSkillsReport:e.agentSkillsReport,agentSkillsError:e.agentSkillsError,agentSkillsAgentId:e.agentSkillsAgentId,skillsFilter:e.skillsFilter,onRefresh:async()=>{await bs(e);const g=e.agentsList?.agents?.map(w=>w.id)??[];g.length>0&&dl(e,g)},onSelectAgent:g=>{e.agentsSelectedId!==g&&(e.agentsSelectedId=g,e.agentFilesList=null,e.agentFilesError=null,e.agentFilesLoading=!1,e.agentFileActive=null,e.agentFileContents={},e.agentFileDrafts={},e.agentSkillsReport=null,e.agentSkillsError=null,e.agentSkillsAgentId=null,cl(e,g),e.agentsPanel==="files"&&$i(e,g),e.agentsPanel==="skills"&&$n(e,g))},onSelectPanel:g=>{e.agentsPanel=g,g==="files"&&v&&e.agentFilesList?.agentId!==v&&(e.agentFilesList=null,e.agentFilesError=null,e.agentFileActive=null,e.agentFileContents={},e.agentFileDrafts={},$i(e,v)),g==="skills"&&v&&$n(e,v),g==="channels"&&oe(e,!1),g==="cron"&&e.loadCron()},onLoadFiles:g=>{(async()=>(await $i(e,g),e.agentFileActive&&await Xa(e,g,e.agentFileActive,{force:!0,preserveDraft:!0})))()},onSelectFile:g=>{e.agentFileActive=g,v&&Xa(e,v,g)},onFileDraftChange:(g,w)=>{e.agentFileDrafts={...e.agentFileDrafts,[g]:w}},onFileReset:g=>{const w=e.agentFileContents[g]??"";e.agentFileDrafts={...e.agentFileDrafts,[g]:w}},onFileSave:g=>{if(!v)return;const w=e.agentFileDrafts[g]??e.agentFileContents[g]??"";yp(e,v,g,w)},onToolsProfileChange:(g,w,_)=>{if(!y)return;const C=y.agents?.list;if(!Array.isArray(C))return;const L=C.findIndex(T=>T&&typeof T=="object"&&"id"in T&&T.id===g);if(L<0)return;const x=["agents","list",L,"tools"];w?q(e,[...x,"profile"],w):ge(e,[...x,"profile"]),_&&ge(e,[...x,"allow"])},onToolsOverridesChange:(g,w,_)=>{if(!y)return;const C=y.agents?.list;if(!Array.isArray(C))return;const L=C.findIndex(T=>T&&typeof T=="object"&&"id"in T&&T.id===g);if(L<0)return;const x=["agents","list",L,"tools"];w.length>0?q(e,[...x,"alsoAllow"],w):ge(e,[...x,"alsoAllow"]),_.length>0?q(e,[...x,"deny"],_):ge(e,[...x,"deny"])},onConfigReload:()=>me(e),onConfigSave:()=>wn(e),onChannelsRefresh:()=>oe(e,!1),onCronRefresh:()=>e.loadCron(),onSkillsFilterChange:g=>e.skillsFilter=g,onSkillsRefresh:()=>{v&&$n(e,v)},onAgentSkillToggle:(g,w,_)=>{if(!y)return;const C=y.agents?.list;if(!Array.isArray(C))return;const L=C.findIndex(Z=>Z&&typeof Z=="object"&&"id"in Z&&Z.id===g);if(L<0)return;const x=C[L],T=w.trim();if(!T)return;const I=e.agentSkillsReport?.skills?.map(Z=>Z.name).filter(Boolean)??[],fe=(Array.isArray(x.skills)?x.skills.map(Z=>String(Z).trim()).filter(Boolean):void 0)??I,G=new Set(fe);_?G.add(T):G.delete(T),q(e,["agents","list",L,"skills"],[...G])},onAgentSkillsClear:g=>{if(!y)return;const w=y.agents?.list;if(!Array.isArray(w))return;const _=w.findIndex(C=>C&&typeof C=="object"&&"id"in C&&C.id===g);_<0||ge(e,["agents","list",_,"skills"])},onAgentSkillsDisableAll:g=>{if(!y)return;const w=y.agents?.list;if(!Array.isArray(w))return;const _=w.findIndex(C=>C&&typeof C=="object"&&"id"in C&&C.id===g);_<0||q(e,["agents","list",_,"skills"],[])},onModelChange:(g,w)=>{if(!y)return;const _=e.agentsList?.defaultId??null;if(_&&g===_){const N=["agents","defaults","model"],G=(y.agents?.defaults??{}).model;if(!w){ge(e,N);return}if(G&&typeof G=="object"&&!Array.isArray(G)){const Z=G.fallbacks,B={primary:w,...Array.isArray(Z)?{fallbacks:Z}:{}};q(e,N,B)}else q(e,N,{primary:w});return}const C=$(g),L=["agents","list",C,"model"];if(!w){ge(e,L);return}const x=(e.configForm??e.configSnapshot?.config)?.agents?.list,I=(Array.isArray(x)&&x[C]?x[C]:null)?.model;if(I&&typeof I=="object"&&!Array.isArray(I)){const N=I.fallbacks,fe={primary:w,...Array.isArray(N)?{fallbacks:N}:{}};q(e,L,fe)}else q(e,L,w)},onModelFallbacksChange:(g,w)=>{if(!y)return;const _=w.map(B=>B.trim()).filter(Boolean),C=e.agentsList?.defaultId??null;if(C&&g===C){const B=["agents","defaults","model"],le=(y.agents?.defaults??{}).model,be=(()=>{if(typeof le=="string")return le.trim()||null;if(le&&typeof le=="object"&&!Array.isArray(le)){const Xt=le.primary;if(typeof Xt=="string")return Xt.trim()||null}return null})();if(_.length===0){be?q(e,B,{primary:be}):ge(e,B);return}q(e,B,be?{primary:be,fallbacks:_}:{fallbacks:_});return}const L=$(g),x=["agents","list",L,"model"],T=(e.configForm??e.configSnapshot?.config)?.agents?.list,N=(Array.isArray(T)&&T[L]?T[L]:null)?.model;if(!N)return;const G=(()=>{if(typeof N=="string")return N.trim()||null;if(N&&typeof N=="object"&&!Array.isArray(N)){const B=N.primary;if(typeof B=="string")return B.trim()||null}return null})();if(_.length===0){G?q(e,x,G):ge(e,x);return}q(e,x,G?{primary:G,fallbacks:_}:{fallbacks:_})}}):m}

        ${e.tab==="skills"?a0({loading:e.skillsLoading,report:e.skillsReport,error:e.skillsError,filter:e.skillsFilter,edits:e.skillEdits,messages:e.skillMessages,busyKey:e.skillsBusyKey,onFilterChange:g=>e.skillsFilter=g,onRefresh:()=>Vt(e,{clearMessages:!0}),onToggle:(g,w)=>Dg(e,g,w),onEdit:(g,w)=>Og(e,g,w),onSaveKey:g=>Bg(e,g),onInstall:(g,w,_)=>Ug(e,g,w,_)}):m}

        ${e.tab==="nodes"?ky({loading:e.nodesLoading,nodes:e.nodes,devicesLoading:e.devicesLoading,devicesError:e.devicesError,devicesList:e.devicesList,configForm:e.configForm??e.configSnapshot?.config,configLoading:e.configLoading,configSaving:e.configSaving,configDirty:e.configFormDirty,configFormMode:e.configFormMode,execApprovalsLoading:e.execApprovalsLoading,execApprovalsSaving:e.execApprovalsSaving,execApprovalsDirty:e.execApprovalsDirty,execApprovalsSnapshot:e.execApprovalsSnapshot,execApprovalsForm:e.execApprovalsForm,execApprovalsSelectedAgent:e.execApprovalsSelectedAgent,execApprovalsTarget:e.execApprovalsTarget,execApprovalsTargetNodeId:e.execApprovalsTargetNodeId,onRefresh:()=>Dn(e),onDevicesRefresh:()=>Be(e),onDeviceApprove:g=>xg(e,g),onDeviceReject:g=>_g(e,g),onDeviceRotate:(g,w,_)=>Cg(e,{deviceId:g,role:w,scopes:_}),onDeviceRevoke:(g,w)=>Eg(e,{deviceId:g,role:w}),onLoadConfig:()=>me(e),onLoadExecApprovals:()=>{const g=e.execApprovalsTarget==="node"&&e.execApprovalsTargetNodeId?{kind:"node",nodeId:e.execApprovalsTargetNodeId}:{kind:"gateway"};return xs(e,g)},onBindDefault:g=>{g?q(e,["tools","exec","node"],g):ge(e,["tools","exec","node"])},onBindAgent:(g,w)=>{const _=["agents","list",g,"tools","exec","node"];w?q(e,_,w):ge(e,_)},onSaveBindings:()=>wn(e),onExecApprovalsTargetChange:(g,w)=>{e.execApprovalsTarget=g,e.execApprovalsTargetNodeId=w,e.execApprovalsSnapshot=null,e.execApprovalsForm=null,e.execApprovalsDirty=!1,e.execApprovalsSelectedAgent=null},onExecApprovalsSelectAgent:g=>{e.execApprovalsSelectedAgent=g},onExecApprovalsPatch:(g,w)=>Mg(e,g,w),onExecApprovalsRemove:g=>Pg(e,g),onSaveExecApprovals:()=>{const g=e.execApprovalsTarget==="node"&&e.execApprovalsTargetNodeId?{kind:"node",nodeId:e.execApprovalsTargetNodeId}:{kind:"gateway"};return Rg(e,g)}}):m}

        ${e.tab==="chat"?ey({sessionKey:e.sessionKey,onSessionKeyChange:g=>{e.sessionKey=g,e.chatMessage="",e.chatAttachments=[],e.chatStream=null,e.chatRunId=null,e.chatStreamStartedAt=null,e.chatQueue=[],e.resetToolStream(),e.resetChatScroll(),e.applySettings({...e.settings,sessionKey:g,lastActiveSessionKey:g}),e.loadAssistantIdentity(),jt(e),zi(e)},thinkingLevel:e.chatThinkingLevel,showThinking:l,loading:e.chatLoading,sending:e.chatSending,assistantAvatarUrl:h,messages:e.chatMessages,toolMessages:e.chatToolMessages,stream:e.chatStream,streamStartedAt:null,draft:e.chatMessage,queue:e.chatQueue,connected:e.connected,canSend:e.connected,disabledReason:s,error:e.lastError,sessions:e.sessionsResult,focusMode:o,onRefresh:()=>Promise.all([jt(e),zi(e)]),onToggleFocusMode:()=>{e.onboarding||e.applySettings({...e.settings,chatFocusMode:!e.settings.chatFocusMode})},onChatScroll:g=>e.handleChatScroll(g),onDraftChange:g=>e.chatMessage=g,attachments:e.chatAttachments,onAttachmentsChange:g=>e.chatAttachments=g,onSend:()=>e.handleSendChat(),canAbort:!!e.chatRunId,onAbort:()=>{e.handleAbortChat()},onQueueRemove:g=>e.removeQueuedMessage(g),onNewSession:()=>e.handleSendChat("/new",{restoreDraft:!0}),showNewMessages:e.chatNewMessagesBelow,onScrollToBottom:()=>e.scrollToBottom(),sidebarOpen:e.sidebarOpen,sidebarContent:e.sidebarContent,sidebarError:e.sidebarError,splitRatio:e.splitRatio,onOpenSidebar:g=>e.handleOpenSidebar(g),onCloseSidebar:()=>e.handleCloseSidebar(),onSplitRatioChange:g=>e.handleSplitRatioChange(g),assistantName:e.assistantName,assistantAvatar:e.assistantAvatar}):m}

        ${e.tab==="config"?oy({raw:e.configRaw,originalRaw:e.configRawOriginal,valid:e.configValid,issues:e.configIssues,loading:e.configLoading,saving:e.configSaving,applying:e.configApplying,updating:e.updateRunning,connected:e.connected,schema:e.configSchema,schemaLoading:e.configSchemaLoading,uiHints:e.configUiHints,formMode:e.configFormMode,formValue:e.configForm,originalValue:e.configFormOriginal,searchQuery:e.configSearchQuery,activeSection:e.configActiveSection,activeSubsection:e.configActiveSubsection,onRawChange:g=>{e.configRaw=g},onFormModeChange:g=>e.configFormMode=g,onFormPatch:(g,w)=>q(e,g,w),onSearchChange:g=>e.configSearchQuery=g,onSectionChange:g=>{e.configActiveSection=g,e.configActiveSubsection=null},onSubsectionChange:g=>e.configActiveSubsection=g,onReload:()=>me(e),onSave:()=>wn(e),onApply:()=>hf(e),onUpdate:()=>pf(e)}):m}

        ${e.tab==="debug"?gy({loading:e.debugLoading,status:e.debugStatus,health:e.debugHealth,models:e.debugModels,heartbeat:e.debugHeartbeat,eventLog:e.eventLog,callMethod:e.debugCallMethod,callParams:e.debugCallParams,callResult:e.debugCallResult,callError:e.debugCallError,onCallMethodChange:g=>e.debugCallMethod=g,onCallParamsChange:g=>e.debugCallParams=g,onRefresh:()=>On(e),onCall:()=>Ff(e)}):m}

        ${e.tab==="logs"?$y({loading:e.logsLoading,error:e.logsError,file:e.logsFile,entries:e.logsEntries,filterText:e.logsFilterText,levelFilters:e.logsLevelFilters,autoFollow:e.logsAutoFollow,truncated:e.logsTruncated,onFilterTextChange:g=>e.logsFilterText=g,onLevelToggle:(g,w)=>{e.logsLevelFilters={...e.logsLevelFilters,[g]:w}},onToggleAutoFollow:g=>e.logsAutoFollow=g,onRefresh:()=>gs(e,{reset:!0}),onExport:(g,w)=>e.exportLogs(g,w),onScroll:g=>e.handleLogsScroll(g)}):m}
      </main>
      ${py(e)}
      ${vy(e)}
    </div>
  `}var u0=Object.create,Ys=Object.defineProperty,f0=Object.getOwnPropertyDescriptor,Br=(e,t)=>(t=Symbol[e])?t:Symbol.for("Symbol."+e),Zt=e=>{throw TypeError(e)},g0=(e,t,n)=>t in e?Ys(e,t,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[t]=n,Go=(e,t)=>Ys(e,"name",{value:t,configurable:!0}),h0=e=>[,,,u0(e?.[Br("metadata")]??null)],Ur=["class","method","getter","setter","accessor","field","value","get","set"],Rt=e=>e!==void 0&&typeof e!="function"?Zt("Function expected"):e,p0=(e,t,n,i,s)=>({kind:Ur[e],name:t,metadata:i,addInitializer:a=>n._?Zt("Already initialized"):s.push(Rt(a||null))}),v0=(e,t)=>g0(t,Br("metadata"),e[3]),f=(e,t,n,i)=>{for(var s=0,a=e[t>>1],o=a&&a.length;s<o;s++)t&1?a[s].call(n):i=a[s].call(n,i);return i},A=(e,t,n,i,s,a)=>{var o,l,d,h,p,u=t&7,y=!!(t&8),v=!!(t&16),$=u>3?e.length+1:u?y?1:2:0,g=Ur[u+5],w=u>3&&(e[$-1]=[]),_=e[$]||(e[$]=[]),C=u&&(!v&&!y&&(s=s.prototype),u<5&&(u>3||!v)&&f0(u<4?s:{get[n](){return Wo(this,a)},set[n](x){return qo(this,a,x)}},n));u?v&&u<4&&Go(a,(u>2?"set ":u>1?"get ":"")+n):Go(s,n);for(var L=i.length-1;L>=0;L--)h=p0(u,n,d={},e[3],_),u&&(h.static=y,h.private=v,p=h.access={has:v?x=>m0(s,x):x=>n in x},u^3&&(p.get=v?x=>(u^1?Wo:b0)(x,s,u^4?a:C.get):x=>x[n]),u>2&&(p.set=v?(x,T)=>qo(x,s,T,u^4?a:C.set):(x,T)=>x[n]=T)),l=(0,i[L])(u?u<4?v?a:C[g]:u>4?void 0:{get:C.get,set:C.set}:s,h),d._=1,u^4||l===void 0?Rt(l)&&(u>4?w.unshift(l):u?v?a=l:C[g]=l:s=l):typeof l!="object"||l===null?Zt("Object expected"):(Rt(o=l.get)&&(C.get=o),Rt(o=l.set)&&(C.set=o),Rt(o=l.init)&&w.unshift(o));return u||v0(e,s),C&&Ys(s,n,C),v?u^4?a:C:s},Qs=(e,t,n)=>t.has(e)||Zt("Cannot "+n),m0=(e,t)=>Object(t)!==t?Zt('Cannot use the "in" operator on this value'):e.has(t),Wo=(e,t,n)=>(Qs(e,t,"read from private field"),n?n.call(e):t.get(e)),qo=(e,t,n,i)=>(Qs(e,t,"write to private field"),i?i.call(e,n):t.set(e,n),n),b0=(e,t,n)=>(Qs(e,t,"access private method"),n),Kr,zr,Hr,jr,Gr,Wr,qr,Vr,Yr,Qr,Jr,Zr,Xr,ec,tc,nc,ic,sc,ac,oc,lc,rc,cc,dc,uc,fc,gc,hc,pc,vc,mc,bc,yc,wc,$c,kc,Ac,Sc,xc,_c,Cc,Ec,Tc,Lc,Ic,Rc,Mc,Pc,Fc,Nc,Oc,Dc,Bc,Uc,Kc,zc,Hc,jc,Gc,Wc,qc,Vc,Yc,Qc,Jc,Zc,Xc,ed,td,nd,id,sd,ad,od,ld,rd,cd,dd,ud,fd,gd,hd,pd,vd,md,bd,yd,wd,$d,kd,Ad,Sd,xd,_d,Cd,Ed,Td,Ld,Id,Rd,Md,Pd,Fd,Nd,Od,Dd,Bd,Ud,Kd,zd,Hd,jd,Gd,Wd,qd,Vd,Yd,Qd,Jd,Zd,Xd,eu,tu,nu,iu,su,au,ou,lu,ru,cu,du,uu,fu,gu,hu,pu,vu,mu,bu,yu,wu,$u,ku,Au,Su,xu,os,_u,c;const Li=jh();function y0(){if(!window.location.search)return!1;const t=new URLSearchParams(window.location.search).get("onboarding");if(!t)return!1;const n=t.trim().toLowerCase();return n==="1"||n==="true"||n==="yes"||n==="on"}_u=[tl("openclaw-app")];class k extends(os=gt,xu=[S()],Su=[S()],Au=[S()],ku=[S()],$u=[S()],wu=[S()],yu=[S()],bu=[S()],mu=[S()],vu=[S()],pu=[S()],hu=[S()],gu=[S()],fu=[S()],uu=[S()],du=[S()],cu=[S()],ru=[S()],lu=[S()],ou=[S()],au=[S()],su=[S()],iu=[S()],nu=[S()],tu=[S()],eu=[S()],Xd=[S()],Zd=[S()],Jd=[S()],Qd=[S()],Yd=[S()],Vd=[S()],qd=[S()],Wd=[S()],Gd=[S()],jd=[S()],Hd=[S()],zd=[S()],Kd=[S()],Ud=[S()],Bd=[S()],Dd=[S()],Od=[S()],Nd=[S()],Fd=[S()],Pd=[S()],Md=[S()],Rd=[S()],Id=[S()],Ld=[S()],Td=[S()],Ed=[S()],Cd=[S()],_d=[S()],xd=[S()],Sd=[S()],Ad=[S()],kd=[S()],$d=[S()],wd=[S()],yd=[S()],bd=[S()],md=[S()],vd=[S()],pd=[S()],hd=[S()],gd=[S()],fd=[S()],ud=[S()],dd=[S()],cd=[S()],rd=[S()],ld=[S()],od=[S()],ad=[S()],sd=[S()],id=[S()],nd=[S()],td=[S()],ed=[S()],Xc=[S()],Zc=[S()],Jc=[S()],Qc=[S()],Yc=[S()],Vc=[S()],qc=[S()],Wc=[S()],Gc=[S()],jc=[S()],Hc=[S()],zc=[S()],Kc=[S()],Uc=[S()],Bc=[S()],Dc=[S()],Oc=[S()],Nc=[S()],Fc=[S()],Pc=[S()],Mc=[S()],Rc=[S()],Ic=[S()],Lc=[S()],Tc=[S()],Ec=[S()],Cc=[S()],_c=[S()],xc=[S()],Sc=[S()],Ac=[S()],kc=[S()],$c=[S()],wc=[S()],yc=[S()],bc=[S()],mc=[S()],vc=[S()],pc=[S()],hc=[S()],gc=[S()],fc=[S()],uc=[S()],dc=[S()],cc=[S()],rc=[S()],lc=[S()],oc=[S()],ac=[S()],sc=[S()],ic=[S()],nc=[S()],tc=[S()],ec=[S()],Xr=[S()],Zr=[S()],Jr=[S()],Qr=[S()],Yr=[S()],Vr=[S()],qr=[S()],Wr=[S()],Gr=[S()],jr=[S()],Hr=[S()],zr=[S()],Kr=[S()],os){constructor(){super(...arguments),this.settings=f(c,8,this,Gg()),f(c,11,this),this.password=f(c,12,this,""),f(c,15,this),this.tab=f(c,16,this,"chat"),f(c,19,this),this.onboarding=f(c,20,this,y0()),f(c,23,this),this.connected=f(c,24,this,!1),f(c,27,this),this.theme=f(c,28,this,this.settings.theme??"system"),f(c,31,this),this.themeResolved=f(c,32,this,"dark"),f(c,35,this),this.hello=f(c,36,this,null),f(c,39,this),this.lastError=f(c,40,this,null),f(c,43,this),this.eventLog=f(c,44,this,[]),f(c,47,this),this.eventLogBuffer=[],this.toolStreamSyncTimer=null,this.sidebarCloseTimer=null,this.assistantName=f(c,48,this,Li.name),f(c,51,this),this.assistantAvatar=f(c,52,this,Li.avatar),f(c,55,this),this.assistantAgentId=f(c,56,this,Li.agentId??null),f(c,59,this),this.sessionKey=f(c,60,this,this.settings.sessionKey),f(c,63,this),this.chatLoading=f(c,64,this,!1),f(c,67,this),this.chatSending=f(c,68,this,!1),f(c,71,this),this.chatMessage=f(c,72,this,""),f(c,75,this),this.chatMessages=f(c,76,this,[]),f(c,79,this),this.chatToolMessages=f(c,80,this,[]),f(c,83,this),this.chatStream=f(c,84,this,null),f(c,87,this),this.chatStreamStartedAt=f(c,88,this,null),f(c,91,this),this.chatRunId=f(c,92,this,null),f(c,95,this),this.compactionStatus=f(c,96,this,null),f(c,99,this),this.chatAvatarUrl=f(c,100,this,null),f(c,103,this),this.chatThinkingLevel=f(c,104,this,null),f(c,107,this),this.chatQueue=f(c,108,this,[]),f(c,111,this),this.chatAttachments=f(c,112,this,[]),f(c,115,this),this.sidebarOpen=f(c,116,this,!1),f(c,119,this),this.sidebarContent=f(c,120,this,null),f(c,123,this),this.sidebarError=f(c,124,this,null),f(c,127,this),this.splitRatio=f(c,128,this,this.settings.splitRatio),f(c,131,this),this.nodesLoading=f(c,132,this,!1),f(c,135,this),this.nodes=f(c,136,this,[]),f(c,139,this),this.devicesLoading=f(c,140,this,!1),f(c,143,this),this.devicesError=f(c,144,this,null),f(c,147,this),this.devicesList=f(c,148,this,null),f(c,151,this),this.execApprovalsLoading=f(c,152,this,!1),f(c,155,this),this.execApprovalsSaving=f(c,156,this,!1),f(c,159,this),this.execApprovalsDirty=f(c,160,this,!1),f(c,163,this),this.execApprovalsSnapshot=f(c,164,this,null),f(c,167,this),this.execApprovalsForm=f(c,168,this,null),f(c,171,this),this.execApprovalsSelectedAgent=f(c,172,this,null),f(c,175,this),this.execApprovalsTarget=f(c,176,this,"gateway"),f(c,179,this),this.execApprovalsTargetNodeId=f(c,180,this,null),f(c,183,this),this.execApprovalQueue=f(c,184,this,[]),f(c,187,this),this.execApprovalBusy=f(c,188,this,!1),f(c,191,this),this.execApprovalError=f(c,192,this,null),f(c,195,this),this.pendingGatewayUrl=f(c,196,this,null),f(c,199,this),this.configLoading=f(c,200,this,!1),f(c,203,this),this.configRaw=f(c,204,this,`{
}
`),f(c,207,this),this.configRawOriginal=f(c,208,this,""),f(c,211,this),this.configValid=f(c,212,this,null),f(c,215,this),this.configIssues=f(c,216,this,[]),f(c,219,this),this.configSaving=f(c,220,this,!1),f(c,223,this),this.configApplying=f(c,224,this,!1),f(c,227,this),this.updateRunning=f(c,228,this,!1),f(c,231,this),this.applySessionKey=f(c,232,this,this.settings.lastActiveSessionKey),f(c,235,this),this.configSnapshot=f(c,236,this,null),f(c,239,this),this.configSchema=f(c,240,this,null),f(c,243,this),this.configSchemaVersion=f(c,244,this,null),f(c,247,this),this.configSchemaLoading=f(c,248,this,!1),f(c,251,this),this.configUiHints=f(c,252,this,{}),f(c,255,this),this.configForm=f(c,256,this,null),f(c,259,this),this.configFormOriginal=f(c,260,this,null),f(c,263,this),this.configFormDirty=f(c,264,this,!1),f(c,267,this),this.configFormMode=f(c,268,this,"form"),f(c,271,this),this.configSearchQuery=f(c,272,this,""),f(c,275,this),this.configActiveSection=f(c,276,this,null),f(c,279,this),this.configActiveSubsection=f(c,280,this,null),f(c,283,this),this.channelsLoading=f(c,284,this,!1),f(c,287,this),this.channelsSnapshot=f(c,288,this,null),f(c,291,this),this.channelsError=f(c,292,this,null),f(c,295,this),this.channelsLastSuccess=f(c,296,this,null),f(c,299,this),this.whatsappLoginMessage=f(c,300,this,null),f(c,303,this),this.whatsappLoginQrDataUrl=f(c,304,this,null),f(c,307,this),this.whatsappLoginConnected=f(c,308,this,null),f(c,311,this),this.whatsappBusy=f(c,312,this,!1),f(c,315,this),this.nostrProfileFormState=f(c,316,this,null),f(c,319,this),this.nostrProfileAccountId=f(c,320,this,null),f(c,323,this),this.presenceLoading=f(c,324,this,!1),f(c,327,this),this.presenceEntries=f(c,328,this,[]),f(c,331,this),this.presenceError=f(c,332,this,null),f(c,335,this),this.presenceStatus=f(c,336,this,null),f(c,339,this),this.agentsLoading=f(c,340,this,!1),f(c,343,this),this.agentsList=f(c,344,this,null),f(c,347,this),this.agentsError=f(c,348,this,null),f(c,351,this),this.agentsSelectedId=f(c,352,this,null),f(c,355,this),this.agentsPanel=f(c,356,this,"overview"),f(c,359,this),this.agentFilesLoading=f(c,360,this,!1),f(c,363,this),this.agentFilesError=f(c,364,this,null),f(c,367,this),this.agentFilesList=f(c,368,this,null),f(c,371,this),this.agentFileContents=f(c,372,this,{}),f(c,375,this),this.agentFileDrafts=f(c,376,this,{}),f(c,379,this),this.agentFileActive=f(c,380,this,null),f(c,383,this),this.agentFileSaving=f(c,384,this,!1),f(c,387,this),this.agentIdentityLoading=f(c,388,this,!1),f(c,391,this),this.agentIdentityError=f(c,392,this,null),f(c,395,this),this.agentIdentityById=f(c,396,this,{}),f(c,399,this),this.agentSkillsLoading=f(c,400,this,!1),f(c,403,this),this.agentSkillsError=f(c,404,this,null),f(c,407,this),this.agentSkillsReport=f(c,408,this,null),f(c,411,this),this.agentSkillsAgentId=f(c,412,this,null),f(c,415,this),this.sessionsLoading=f(c,416,this,!1),f(c,419,this),this.sessionsResult=f(c,420,this,null),f(c,423,this),this.sessionsError=f(c,424,this,null),f(c,427,this),this.sessionsFilterActive=f(c,428,this,""),f(c,431,this),this.sessionsFilterLimit=f(c,432,this,"120"),f(c,435,this),this.sessionsIncludeGlobal=f(c,436,this,!0),f(c,439,this),this.sessionsIncludeUnknown=f(c,440,this,!1),f(c,443,this),this.cronLoading=f(c,444,this,!1),f(c,447,this),this.cronJobs=f(c,448,this,[]),f(c,451,this),this.cronStatus=f(c,452,this,null),f(c,455,this),this.cronError=f(c,456,this,null),f(c,459,this),this.cronForm=f(c,460,this,{...Uh}),f(c,463,this),this.cronRunsJobId=f(c,464,this,null),f(c,467,this),this.cronRuns=f(c,468,this,[]),f(c,471,this),this.cronBusy=f(c,472,this,!1),f(c,475,this),this.skillsLoading=f(c,476,this,!1),f(c,479,this),this.skillsReport=f(c,480,this,null),f(c,483,this),this.skillsError=f(c,484,this,null),f(c,487,this),this.skillsFilter=f(c,488,this,""),f(c,491,this),this.skillEdits=f(c,492,this,{}),f(c,495,this),this.skillsBusyKey=f(c,496,this,null),f(c,499,this),this.skillMessages=f(c,500,this,{}),f(c,503,this),this.debugLoading=f(c,504,this,!1),f(c,507,this),this.debugStatus=f(c,508,this,null),f(c,511,this),this.debugHealth=f(c,512,this,null),f(c,515,this),this.debugModels=f(c,516,this,[]),f(c,519,this),this.debugHeartbeat=f(c,520,this,null),f(c,523,this),this.debugCallMethod=f(c,524,this,""),f(c,527,this),this.debugCallParams=f(c,528,this,"{}"),f(c,531,this),this.debugCallResult=f(c,532,this,null),f(c,535,this),this.debugCallError=f(c,536,this,null),f(c,539,this),this.logsLoading=f(c,540,this,!1),f(c,543,this),this.logsError=f(c,544,this,null),f(c,547,this),this.logsFile=f(c,548,this,null),f(c,551,this),this.logsEntries=f(c,552,this,[]),f(c,555,this),this.logsFilterText=f(c,556,this,""),f(c,559,this),this.logsLevelFilters=f(c,560,this,{...Bh}),f(c,563,this),this.logsAutoFollow=f(c,564,this,!0),f(c,567,this),this.logsTruncated=f(c,568,this,!1),f(c,571,this),this.logsCursor=f(c,572,this,null),f(c,575,this),this.logsLastFetchAt=f(c,576,this,null),f(c,579,this),this.logsLimit=f(c,580,this,500),f(c,583,this),this.logsMaxBytes=f(c,584,this,25e4),f(c,587,this),this.logsAtBottom=f(c,588,this,!0),f(c,591,this),this.client=null,this.chatScrollFrame=null,this.chatScrollTimeout=null,this.chatHasAutoScrolled=!1,this.chatUserNearBottom=!0,this.chatNewMessagesBelow=f(c,592,this,!1),f(c,595,this),this.nodesPollInterval=null,this.logsPollInterval=null,this.debugPollInterval=null,this.logsScrollFrame=null,this.toolStreamById=new Map,this.toolStreamOrder=[],this.refreshSessionsAfterChat=new Set,this.basePath="",this.popStateHandler=()=>oh(this),this.themeMedia=null,this.themeMediaHandler=null,this.topbarObserver=null}createRenderRoot(){return this}connectedCallback(){super.connectedCallback(),tp(this)}firstUpdated(){np(this)}disconnectedCallback(){ip(this),super.disconnectedCallback()}updated(t){sp(this,t)}connect(){Ql(this)}handleChatScroll(t){If(this,t)}handleLogsScroll(t){Rf(this,t)}exportLogs(t,n){Mf(t,n)}resetToolStream(){Hn(this)}resetChatScroll(){Ra(this)}scrollToBottom(){Ra(this),Wt(this,!0)}async loadAssistantIdentity(){await ql(this)}applySettings(t){Oe(this,t)}setTab(t){Xg(this,t)}setTheme(t,n){eh(this,t,n)}async loadOverview(){await Bl(this)}async loadCron(){await Tn(this)}async handleAbortChat(){await Hl(this)}removeQueuedMessage(t){Ph(this,t)}async handleSendChat(t,n){await Fh(this,t,n)}async handleWhatsAppStart(t){await yf(this,t)}async handleWhatsAppWait(){await wf(this)}async handleWhatsAppLogout(){await $f(this)}async handleChannelConfigSave(){await kf(this)}async handleChannelConfigReload(){await Af(this)}handleNostrProfileEdit(t,n){xf(this,t,n)}handleNostrProfileCancel(){_f(this)}handleNostrProfileFieldChange(t,n){Cf(this,t,n)}async handleNostrProfileSave(){await Tf(this)}async handleNostrProfileImport(){await Lf(this)}handleNostrProfileToggleAdvanced(){Ef(this)}async handleExecApprovalDecision(t){const n=this.execApprovalQueue[0];if(!(!n||!this.client||this.execApprovalBusy)){this.execApprovalBusy=!0,this.execApprovalError=null;try{await this.client.request("exec.approval.resolve",{id:n.id,decision:t}),this.execApprovalQueue=this.execApprovalQueue.filter(i=>i.id!==n.id)}catch(i){this.execApprovalError=`Exec approval failed: ${String(i)}`}finally{this.execApprovalBusy=!1}}}handleGatewayUrlConfirm(){const t=this.pendingGatewayUrl;t&&(this.pendingGatewayUrl=null,Oe(this,{...this.settings,gatewayUrl:t}),this.connect())}handleGatewayUrlCancel(){this.pendingGatewayUrl=null}handleOpenSidebar(t){this.sidebarCloseTimer!=null&&(window.clearTimeout(this.sidebarCloseTimer),this.sidebarCloseTimer=null),this.sidebarContent=t,this.sidebarError=null,this.sidebarOpen=!0}handleCloseSidebar(){this.sidebarOpen=!1,this.sidebarCloseTimer!=null&&window.clearTimeout(this.sidebarCloseTimer),this.sidebarCloseTimer=window.setTimeout(()=>{this.sidebarOpen||(this.sidebarContent=null,this.sidebarError=null,this.sidebarCloseTimer=null)},200)}handleSplitRatioChange(t){const n=Math.max(.4,Math.min(.7,t));this.splitRatio=n,this.applySettings({...this.settings,splitRatio:n})}render(){return d0(this)}}c=h0(os);A(c,5,"settings",xu,k);A(c,5,"password",Su,k);A(c,5,"tab",Au,k);A(c,5,"onboarding",ku,k);A(c,5,"connected",$u,k);A(c,5,"theme",wu,k);A(c,5,"themeResolved",yu,k);A(c,5,"hello",bu,k);A(c,5,"lastError",mu,k);A(c,5,"eventLog",vu,k);A(c,5,"assistantName",pu,k);A(c,5,"assistantAvatar",hu,k);A(c,5,"assistantAgentId",gu,k);A(c,5,"sessionKey",fu,k);A(c,5,"chatLoading",uu,k);A(c,5,"chatSending",du,k);A(c,5,"chatMessage",cu,k);A(c,5,"chatMessages",ru,k);A(c,5,"chatToolMessages",lu,k);A(c,5,"chatStream",ou,k);A(c,5,"chatStreamStartedAt",au,k);A(c,5,"chatRunId",su,k);A(c,5,"compactionStatus",iu,k);A(c,5,"chatAvatarUrl",nu,k);A(c,5,"chatThinkingLevel",tu,k);A(c,5,"chatQueue",eu,k);A(c,5,"chatAttachments",Xd,k);A(c,5,"sidebarOpen",Zd,k);A(c,5,"sidebarContent",Jd,k);A(c,5,"sidebarError",Qd,k);A(c,5,"splitRatio",Yd,k);A(c,5,"nodesLoading",Vd,k);A(c,5,"nodes",qd,k);A(c,5,"devicesLoading",Wd,k);A(c,5,"devicesError",Gd,k);A(c,5,"devicesList",jd,k);A(c,5,"execApprovalsLoading",Hd,k);A(c,5,"execApprovalsSaving",zd,k);A(c,5,"execApprovalsDirty",Kd,k);A(c,5,"execApprovalsSnapshot",Ud,k);A(c,5,"execApprovalsForm",Bd,k);A(c,5,"execApprovalsSelectedAgent",Dd,k);A(c,5,"execApprovalsTarget",Od,k);A(c,5,"execApprovalsTargetNodeId",Nd,k);A(c,5,"execApprovalQueue",Fd,k);A(c,5,"execApprovalBusy",Pd,k);A(c,5,"execApprovalError",Md,k);A(c,5,"pendingGatewayUrl",Rd,k);A(c,5,"configLoading",Id,k);A(c,5,"configRaw",Ld,k);A(c,5,"configRawOriginal",Td,k);A(c,5,"configValid",Ed,k);A(c,5,"configIssues",Cd,k);A(c,5,"configSaving",_d,k);A(c,5,"configApplying",xd,k);A(c,5,"updateRunning",Sd,k);A(c,5,"applySessionKey",Ad,k);A(c,5,"configSnapshot",kd,k);A(c,5,"configSchema",$d,k);A(c,5,"configSchemaVersion",wd,k);A(c,5,"configSchemaLoading",yd,k);A(c,5,"configUiHints",bd,k);A(c,5,"configForm",md,k);A(c,5,"configFormOriginal",vd,k);A(c,5,"configFormDirty",pd,k);A(c,5,"configFormMode",hd,k);A(c,5,"configSearchQuery",gd,k);A(c,5,"configActiveSection",fd,k);A(c,5,"configActiveSubsection",ud,k);A(c,5,"channelsLoading",dd,k);A(c,5,"channelsSnapshot",cd,k);A(c,5,"channelsError",rd,k);A(c,5,"channelsLastSuccess",ld,k);A(c,5,"whatsappLoginMessage",od,k);A(c,5,"whatsappLoginQrDataUrl",ad,k);A(c,5,"whatsappLoginConnected",sd,k);A(c,5,"whatsappBusy",id,k);A(c,5,"nostrProfileFormState",nd,k);A(c,5,"nostrProfileAccountId",td,k);A(c,5,"presenceLoading",ed,k);A(c,5,"presenceEntries",Xc,k);A(c,5,"presenceError",Zc,k);A(c,5,"presenceStatus",Jc,k);A(c,5,"agentsLoading",Qc,k);A(c,5,"agentsList",Yc,k);A(c,5,"agentsError",Vc,k);A(c,5,"agentsSelectedId",qc,k);A(c,5,"agentsPanel",Wc,k);A(c,5,"agentFilesLoading",Gc,k);A(c,5,"agentFilesError",jc,k);A(c,5,"agentFilesList",Hc,k);A(c,5,"agentFileContents",zc,k);A(c,5,"agentFileDrafts",Kc,k);A(c,5,"agentFileActive",Uc,k);A(c,5,"agentFileSaving",Bc,k);A(c,5,"agentIdentityLoading",Dc,k);A(c,5,"agentIdentityError",Oc,k);A(c,5,"agentIdentityById",Nc,k);A(c,5,"agentSkillsLoading",Fc,k);A(c,5,"agentSkillsError",Pc,k);A(c,5,"agentSkillsReport",Mc,k);A(c,5,"agentSkillsAgentId",Rc,k);A(c,5,"sessionsLoading",Ic,k);A(c,5,"sessionsResult",Lc,k);A(c,5,"sessionsError",Tc,k);A(c,5,"sessionsFilterActive",Ec,k);A(c,5,"sessionsFilterLimit",Cc,k);A(c,5,"sessionsIncludeGlobal",_c,k);A(c,5,"sessionsIncludeUnknown",xc,k);A(c,5,"cronLoading",Sc,k);A(c,5,"cronJobs",Ac,k);A(c,5,"cronStatus",kc,k);A(c,5,"cronError",$c,k);A(c,5,"cronForm",wc,k);A(c,5,"cronRunsJobId",yc,k);A(c,5,"cronRuns",bc,k);A(c,5,"cronBusy",mc,k);A(c,5,"skillsLoading",vc,k);A(c,5,"skillsReport",pc,k);A(c,5,"skillsError",hc,k);A(c,5,"skillsFilter",gc,k);A(c,5,"skillEdits",fc,k);A(c,5,"skillsBusyKey",uc,k);A(c,5,"skillMessages",dc,k);A(c,5,"debugLoading",cc,k);A(c,5,"debugStatus",rc,k);A(c,5,"debugHealth",lc,k);A(c,5,"debugModels",oc,k);A(c,5,"debugHeartbeat",ac,k);A(c,5,"debugCallMethod",sc,k);A(c,5,"debugCallParams",ic,k);A(c,5,"debugCallResult",nc,k);A(c,5,"debugCallError",tc,k);A(c,5,"logsLoading",ec,k);A(c,5,"logsError",Xr,k);A(c,5,"logsFile",Zr,k);A(c,5,"logsEntries",Jr,k);A(c,5,"logsFilterText",Qr,k);A(c,5,"logsLevelFilters",Yr,k);A(c,5,"logsAutoFollow",Vr,k);A(c,5,"logsTruncated",qr,k);A(c,5,"logsCursor",Wr,k);A(c,5,"logsLastFetchAt",Gr,k);A(c,5,"logsLimit",jr,k);A(c,5,"logsMaxBytes",Hr,k);A(c,5,"logsAtBottom",zr,k);A(c,5,"chatNewMessagesBelow",Kr,k);k=A(c,0,"OpenClawApp",_u,k);f(c,1,k);
//# sourceMappingURL=index-C_TY5Tiw.js.map
