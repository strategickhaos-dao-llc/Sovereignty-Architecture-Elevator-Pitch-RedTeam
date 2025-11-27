import { ethers, network } from "hardhat";
import * as fs from "fs";
import * as path from "path";

/**
 * Deployment script for Strategickhaos DAO Irrevocable Charity Splitter
 * 
 * This deploys:
 * 1. MerkleCharityDistributor - The charity treasury receiving 7%
 * 2. IrrevocableCharitySplitter - The main splitter contract (93% ops / 7% charity)
 * 
 * Default charities (GiveWell top charities):
 * - Against Malaria Foundation
 * - Helen Keller International
 * - Malaria Consortium
 * - New Incentives
 */

interface DeploymentInfo {
  network: string;
  chainId: number;
  deployer: string;
  timestamp: string;
  contracts: {
    merkleCharityDistributor: {
      address: string;
      rootUpdater: string;
    };
    irrevocableCharitySplitter: {
      address: string;
      operationsMultisig: string;
      charityTreasury: string;
      charityBps: number;
      operationsBps: number;
    };
  };
  defaultCharities: Array<{
    name: string;
    ein: string;
    allocationBps: number;
  }>;
}

// GiveWell recommended charities (update with real addresses in production)
const DEFAULT_CHARITIES = [
  {
    name: "Against Malaria Foundation",
    ein: "20-8521450",
    allocationBps: 2500, // 25% of charity allocation
  },
  {
    name: "Helen Keller International",
    ein: "13-5562162",
    allocationBps: 2500, // 25% of charity allocation
  },
  {
    name: "Malaria Consortium",
    ein: "98-0627052",
    allocationBps: 2500, // 25% of charity allocation
  },
  {
    name: "New Incentives",
    ein: "45-3321264",
    allocationBps: 2500, // 25% of charity allocation
  },
];

async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║  STRATEGICKHAOS DAO - IRREVOCABLE CHARITY SPLITTER DEPLOY  ║");
  console.log("╠════════════════════════════════════════════════════════════╣");
  console.log("║  7% GUARANTEED TO CHARITY - FOREVER - NO RUG PULLS         ║");
  console.log("╚════════════════════════════════════════════════════════════╝");
  console.log("");

  const [deployer] = await ethers.getSigners();
  const chainId = (await ethers.provider.getNetwork()).chainId;

  console.log(`Network: ${network.name} (chainId: ${chainId})`);
  console.log(`Deployer: ${deployer.address}`);
  console.log(`Balance: ${ethers.formatEther(await ethers.provider.getBalance(deployer.address))} ETH`);
  console.log("");

  // Get configuration from environment or use defaults
  const OPERATIONS_MULTISIG = process.env.OPERATIONS_MULTISIG || deployer.address;
  const ROOT_UPDATER = process.env.ROOT_UPDATER || deployer.address;

  console.log("Configuration:");
  console.log(`  Operations Multisig: ${OPERATIONS_MULTISIG}`);
  console.log(`  Root Updater: ${ROOT_UPDATER}`);
  console.log("");

  // Step 1: Deploy MerkleCharityDistributor
  console.log("Step 1/2: Deploying MerkleCharityDistributor...");
  const MerkleCharityDistributor = await ethers.getContractFactory("MerkleCharityDistributor");
  const charityDistributor = await MerkleCharityDistributor.deploy(ROOT_UPDATER);
  await charityDistributor.waitForDeployment();
  const charityDistributorAddress = await charityDistributor.getAddress();
  console.log(`  ✓ MerkleCharityDistributor deployed: ${charityDistributorAddress}`);
  console.log("");

  // Step 2: Deploy IrrevocableCharitySplitter
  console.log("Step 2/2: Deploying IrrevocableCharitySplitter...");
  const IrrevocableCharitySplitter = await ethers.getContractFactory("IrrevocableCharitySplitter");
  const charitySplitter = await IrrevocableCharitySplitter.deploy(
    OPERATIONS_MULTISIG,
    charityDistributorAddress
  );
  await charitySplitter.waitForDeployment();
  const charitySplitterAddress = await charitySplitter.getAddress();
  console.log(`  ✓ IrrevocableCharitySplitter deployed: ${charitySplitterAddress}`);
  console.log("");

  // Verify deployment
  console.log("Verifying deployment...");
  const verifyCharity = await charitySplitter.verifyCharityPercentage();
  console.log(`  ✓ Charity percentage verified: ${verifyCharity ? "7% LOCKED" : "ERROR"}`);
  
  const deployedAt = await charitySplitter.deployedAt();
  console.log(`  ✓ Deployed at timestamp: ${deployedAt.toString()}`);
  console.log("");

  // Save deployment info
  const deploymentInfo: DeploymentInfo = {
    network: network.name,
    chainId: Number(chainId),
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      merkleCharityDistributor: {
        address: charityDistributorAddress,
        rootUpdater: ROOT_UPDATER,
      },
      irrevocableCharitySplitter: {
        address: charitySplitterAddress,
        operationsMultisig: OPERATIONS_MULTISIG,
        charityTreasury: charityDistributorAddress,
        charityBps: 700,
        operationsBps: 9300,
      },
    },
    defaultCharities: DEFAULT_CHARITIES,
  };

  const deploymentsDir = path.join(__dirname, "../deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }

  const deploymentPath = path.join(deploymentsDir, `${network.name}-${chainId}.json`);
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log(`Deployment info saved to: ${deploymentPath}`);
  console.log("");

  // Print summary
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║                   DEPLOYMENT SUMMARY                       ║");
  console.log("╠════════════════════════════════════════════════════════════╣");
  console.log(`║  Splitter:     ${charitySplitterAddress}  ║`);
  console.log(`║  Distributor:  ${charityDistributorAddress}  ║`);
  console.log("╠════════════════════════════════════════════════════════════╣");
  console.log("║  93% → Operations Multisig                                 ║");
  console.log("║   7% → Charity Treasury (IRREVOCABLE)                      ║");
  console.log("╚════════════════════════════════════════════════════════════╝");
  console.log("");
  console.log("Next steps:");
  console.log("  1. Verify contracts on Basescan: npm run verify");
  console.log("  2. Register charities with their wallet addresses");
  console.log("  3. Update operations multisig to a proper multisig wallet");
  console.log("  4. Send funds to the splitter to test the 93/7 split");
  console.log("");

  return deploymentInfo;
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
