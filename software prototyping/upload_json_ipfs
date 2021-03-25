const ipfs = require("nano-ipfs-store").at("https://ipfs.infura.io:5001");

(async () => {

  const doc = JSON.stringify({
    foo: "bar",
    tic: "tac"
  });
  
  const cid = await ipfs.add(doc);

  console.log("IPFS cid:", cid);
  
  console.log(await ipfs.cat(cid));

})();
