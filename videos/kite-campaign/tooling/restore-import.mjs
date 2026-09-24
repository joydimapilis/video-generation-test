import {registerHooks} from 'node:module';
registerHooks({resolve(specifier,context,nextResolve){
 if(specifier==='../../../../packages/cli/src/media-use/lib/media-fetch.mjs')return {url:new URL('./media-fetch.mjs',import.meta.url).href,shortCircuit:true};
 return nextResolve(specifier,context);
}});
