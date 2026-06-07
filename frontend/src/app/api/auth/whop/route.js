import { NextResponse } from 'next/server';
import Whop from '@whop/sdk';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  if (!code) {
    return NextResponse.json({ error: 'Missing OAuth code' }, { status: 400 });
  }

  try {
    const client = new Whop({ apiKey: process.env.WHOP_API_KEY });

    // In a real application, you would exchange the code for a token
    // For this prototype, we confirm the flow setup

    return NextResponse.json({
      success: true,
      message: 'OAuth flow established with Whop',
      action: 'Redirecting to dashboard...'
    });
  } catch (error) {
    console.error('Whop Auth Error:', error);
    return NextResponse.json({ error: 'Authentication failed' }, { status: 500 });
  }
}
